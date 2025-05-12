"""
This module defines a set of functions to aggregate operational metrics related to hospital admissions, discharges, MDT meetings,
appointments, treatment start times, and bed occupancy. It performs calculations on these metrics using data from the primary database
and stores the results in a secondary metrics database.

Metrics aggregated:
1. **Daily Admissions and Discharges**: The total number of admissions and discharges on a given day.
2. **Average Length of Stay**: The average number of days patients stay in the hospital.
3. **Average MDT Wait Time**: The average wait time (in days) from referral to review in MDT meetings.
4. **Readmission Rate (30 days)**: The number of readmissions within 30 days of discharge.
5. **Appointment No-Show Rate**: The percentage of appointments that were missed or canceled.
6. **Bed Occupancy Rate**: The percentage of hospital beds occupied on a given day.
7. **Admission to Treatment Start Time**: The average number of days between patient admission and the start of treatment.

The module expects SQLAlchemy sessions for querying the database.
"""
from datetime import datetime
from typing import Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.admissions import ReferralAdmission
from app.models.appointments import Appointment
from app.models.mdt import MDTMeeting
from app.models.metrics import OperationalMetrics
from app.models.treatments import Treatment  # Assuming this exists
from app.models.patient import Patient

TOTAL_BEDS = 100  # Placeholder for real-time config or DB-driven count

def get_admissions_discharge_counts(session: Session, date_: datetime.date) -> Tuple[int, int]:
    """
    Fetches the daily count of admissions and discharges for a specific date.

    Args:
        session (Session): The SQLAlchemy session to query the database.
        date_ (datetime.date): The date for which the admissions and discharges are being counted.

    Returns:
        Tuple[int, int]: A tuple containing the count of daily admissions and discharges.
    """
    admissions = session.query(func.count()).filter(func.date(ReferralAdmission.admit_time) == date_).scalar()
    discharges = session.query(func.count()).filter(func.date(ReferralAdmission.discharge_time) == date_).scalar()
    return admissions, discharges

def calculate_avg_length_of_stay(session: Session) -> float:
    """
    Calculates the average length of stay (LOS) for patients who have been discharged.

    Args:
        session (Session): The SQLAlchemy session to query the database.

    Returns:
        float: The average length of stay in days.
    """
    stays = session.query(ReferralAdmission).filter(ReferralAdmission.discharge_time.isnot(None)).all()
    los_list = [(a.discharge_time - a.admit_time).days for a in stays if a.admit_time and a.discharge_time]
    return sum(los_list) / len(los_list) if los_list else 0

def calculate_avg_mdt_wait_time(session: Session) -> float:
    """
    Calculates the average wait time (in days) between the referral and review times for MDT meetings.

    Args:
        session (Session): The SQLAlchemy session to query the database.

    Returns:
        float: The average wait time in days.
    """
    meetings = session.query(MDTMeeting).filter(
        MDTMeeting.referral_time.isnot(None), MDTMeeting.review_time.isnot(None)
    ).all()
    wait_days = [(m.review_time - m.referral_time).days for m in meetings]
    return sum(wait_days) / len(wait_days) if wait_days else 0

def calculate_readmissions(session: Session, days: int = 30) -> int:
    """
    Calculates the number of readmissions for patients within a specified number of days (default is 30 days).

    Args:
        session (Session): The SQLAlchemy session to query the database.
        days (int, optional): The number of days within which a patient is considered to have been readmitted. Defaults to 30.

    Returns:
        int: The number of readmissions within the specified period.
    """
    admissions = session.query(ReferralAdmission).order_by(ReferralAdmission.patient_id, ReferralAdmission.admit_time).all()

    last_admit = {}
    count = 0
    for a in admissions:
        if a.patient_id in last_admit:
            delta = (a.admit_time - last_admit[a.patient_id]).days
            if 0 < delta <= days:
                count += 1
        if a.discharge_time:
            last_admit[a.patient_id] = a.discharge_time
    return count

def calculate_no_show_rate(session: Session) -> float:
    """
    Calculates the no-show rate for appointments as the percentage of appointments missed or canceled.

    Args:
        session (Session): The SQLAlchemy session to query the database.

    Returns:
        float: The no-show rate as a percentage.
    """
    appts = session.query(Appointment).all()
    total = len(appts)
    missed = sum(1 for a in appts if not a.attended or a.cancelled)
    return (missed / total) * 100 if total else 0

def calculate_bed_occupancy(session: Session, date_: datetime.date, total_beds: int = TOTAL_BEDS) -> float:
    """
    Calculates the bed occupancy rate for a specific date, given the total number of available beds.

    Args:
        session (Session): The SQLAlchemy session to query the database.
        date_ (datetime.date): The date for which the bed occupancy rate is calculated.
        total_beds (int, optional): The total number of beds available in the hospital. Defaults to 100.

    Returns:
        float: The bed occupancy rate as a percentage.
    """
    occupied = session.query(func.count()).filter(
        ReferralAdmission.admit_time <= date_,
        func.coalesce(ReferralAdmission.discharge_time, date_) >= date_
    ).scalar()
    return (occupied / total_beds) * 100

def calculate_admit_to_treatment_time(session: Session) -> float:
    """
    Calculates the average time (in days) from patient admission to the start of treatment.

    Args:
        session (Session): The SQLAlchemy session to query the database.

    Returns:
        float: The average time in days from admission to treatment start.
    """
    pairs = session.query(ReferralAdmission.admit_time, Treatment.start_time).join(
        Treatment, Treatment.patient_id == ReferralAdmission.patient_id
    ).filter(Treatment.start_time.isnot(None)).all()

    gaps = [(start - admit).days for admit, start in pairs if start and admit]
    return sum(gaps) / len(gaps) if gaps else 0

def aggregate_operational_metrics():
    """
    Aggregates various operational metrics for the hospital, including admissions,
    discharges, length of stay, MDT wait time, readmissions, no-show rate, bed occupancy,
    and treatment start time. The metrics are calculated using data from the primary database
    and stored in the metrics database.

    Args:
        None

    Returns:
        None: This function does not return any value. It stores the aggregated metrics in
        the metrics database.
    """
    from app.database.primary import PrimarySessionLocal
    from app.database.metrics import MetricsSessionLocal

    today = datetime.today().date()

    with PrimarySessionLocal() as source_db:
        daily_adm, daily_dis = get_admissions_discharge_counts(source_db, today)
        avg_los = calculate_avg_length_of_stay(source_db)
        avg_mdt_wait = calculate_avg_mdt_wait_time(source_db)
        readmissions = calculate_readmissions(source_db)
        no_show = calculate_no_show_rate(source_db)
        bed_occ = calculate_bed_occupancy(source_db, today)
        admit_to_treat = calculate_admit_to_treatment_time(source_db)

    with MetricsSessionLocal() as metrics_db:
        def save_metric(name: str, value: float, unit: str = "count"):
            metric = OperationalMetrics(date=today, metric_name=name, value=value, unit=unit)
            metrics_db.add(metric)

        save_metric("daily_admissions", daily_adm)
        save_metric("daily_discharges", daily_dis)
        save_metric("average_length_of_stay", avg_los, "days")
        save_metric("average_mdt_wait_time", avg_mdt_wait, "days")
        save_metric("readmission_rate_30d", readmissions)
        save_metric("appointment_no_show_rate", no_show, "percent")
        save_metric("bed_occupancy_rate", bed_occ, "percent")
        save_metric("admission_to_treatment_start", admit_to_treat, "days")

        metrics_db.commit()
