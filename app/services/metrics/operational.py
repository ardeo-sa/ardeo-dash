"""
This module defines a set of functions to aggregate operational metrics related to hospital admissions, discharges,
MDT meetings, appointments, treatment start times, and bed occupancy. It performs calculations on these metrics using
data from the primary database.

Metrics calculated:
1. Daily Admissions and Discharges**: The total number of admissions and discharges on a given day.
2. Average Length of Stay: The average number of days patients stay in the hospital.
3. Average MDT Wait Time: The average wait time (in days) from referral to review in MDT meetings.
4. Readmission Rate (30 days): The number of readmissions within 30 days of discharge.
5. Appointment No-Show Rate: The percentage of appointments that were missed or canceled.
6. Bed Occupancy Rate: The percentage of hospital beds occupied on a given day.
7. Admission to Treatment Start Time: The average number of days between patient admission and the start of treatment.

The module expects SQLAlchemy sessions for querying the database. This module does NOT handle persistence of metrics.
"""
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any

from sqlalchemy import func
from sqlalchemy.orm import Session

# from app.database.primary import PrimarySessionLocal
# from app.database.metrics import MetricsSessionLocal

from app.models.admissions import ReferralAdmission
from app.models.appointments import Appointment
from app.models.mdt import MDTMeeting
# from app.models.metrics import OperationalMetrics
from app.models.treatments import Treatment
# from app.models.patient import Patient

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

    start = datetime.combine(date_, datetime.min.time())
    end = start + timedelta(days=1)

    admissions = session.query(ReferralAdmission).filter(
        ReferralAdmission.admit_time >= start,
        ReferralAdmission.admit_time < end
    ).count()

    discharges = session.query(ReferralAdmission).filter(
        ReferralAdmission.discharge_time >= start,
        ReferralAdmission.discharge_time < end
    ).count()

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
        MDTMeeting.referral_time.isnot(None),
        MDTMeeting.review_time.isnot(None)
    ).all()
    wait_days = [(m.review_time - m.referral_time).days for m in meetings]
    return sum(wait_days) / len(wait_days) if wait_days else 0


def calculate_readmissions(session: Session, days: int = 30) -> int:
    """
    Calculates the number of readmissions for patients within a specified number of days (default is 30 days).

    Args:
        session (Session): The SQLAlchemy session to query the database.
        days (int, optional): The number of days within which a patient is considered to have been readmitted.
        Defaults to 30.

    Returns:
        int: The number of readmissions within the specified period.
    """
    admissions = session.query(ReferralAdmission).order_by(
        ReferralAdmission.patient_id,
        ReferralAdmission.admit_time
    ).all()

    last_discharge = {}
    count = 0

    for a in admissions:
        if a.patient_id in last_discharge and a.admit_time > last_discharge[a.patient_id]:
            delta = (a.admit_time - last_discharge[a.patient_id]).days
            if 0 < delta <= days:
                count += 1

        if a.discharge_time:
            last_discharge[a.patient_id] = a.discharge_time
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
    no_shows = sum(1 for a in appts if not a.attended and not a.cancelled)
    return (no_shows / total) * 100 if total else 0

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
    occupied = session.query(ReferralAdmission).filter(
        ReferralAdmission.admit_time <= date_,
        func.coalesce(ReferralAdmission.discharge_time, date_) >= date_
    ).count()

    return (occupied / total_beds) * 100

def calculate_admit_to_treatment_time(session: Session) -> float:
    """
    Calculates the average time (in days) from patient admission to the start of treatment.

    Args:
        session (Session): The SQLAlchemy session to query the database.

    Returns:
        float: The average time in days from admission to treatment start.
    """
    pairs = session.query(
        ReferralAdmission.admit_time,
        Treatment.start_time
    ).join(
        Treatment, Treatment.patient_id == ReferralAdmission.patient_id
    ).filter(
        Treatment.start_time.isnot(None)
    ).all()

    gaps = [(start - admit).days for admit, start in pairs if start > admit]
    return sum(gaps) / len(gaps) if gaps else 0

def aggregate_operational_metrics(session: Session, date_: datetime.date = None) -> Dict[str, Any]:
    """
    Computes all operational metrics for a given date.

    Args:
        session (Session): The SQLAlchemy session to query the database.
        date_ (datetime.date, optional): The date for which metrics are calculated. Defaults to today.

    Returns:
        Dict[str, Any]: A dictionary containing metric names and their computed values.
    """
    date_ = date_ or datetime.today().date()

    admissions, discharges = get_admissions_discharge_counts(session, date_)
    return {
        "date": date_,
        "daily_admissions": admissions,
        "daily_discharges": discharges,
        "average_length_of_stay": calculate_avg_length_of_stay(session),
        "average_mdt_wait_time": calculate_avg_mdt_wait_time(session),
        "readmission_rate_30d": calculate_readmissions(session),
        "appointment_no_show_rate": calculate_no_show_rate(session),
        "bed_occupancy_rate": calculate_bed_occupancy(session, date_),
        "admission_to_treatment_start": calculate_admit_to_treatment_time(session),
    }
