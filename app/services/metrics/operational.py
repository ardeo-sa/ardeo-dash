from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Tuple, List

from app.models.admission import Admission
from app.models.mdt import MDTMeeting
from app.models.appointments import Appointment
from app.models.treatments import Treatment  # Assuming this exists
from app.models.metrics import OperationalMetrics

TOTAL_BEDS = 100  # Placeholder for real-time config or DB-driven count


def get_admissions_discharge_counts(session: Session, date_: datetime.date) -> Tuple[int, int]:
    admissions = session.query(func.count()).filter(func.date(Admission.admit_time) == date_).scalar()
    discharges = session.query(func.count()).filter(func.date(Admission.discharge_time) == date_).scalar()
    return admissions, discharges


def calculate_avg_length_of_stay(session: Session) -> float:
    stays = session.query(Admission).filter(Admission.discharge_time.isnot(None)).all()
    los_list = [(a.discharge_time - a.admit_time).days for a in stays if a.admit_time and a.discharge_time]
    return sum(los_list) / len(los_list) if los_list else 0


def calculate_avg_mdt_wait_time(session: Session) -> float:
    meetings = session.query(MDTMeeting).filter(
        MDTMeeting.referral_time.isnot(None), MDTMeeting.review_time.isnot(None)
    ).all()
    wait_days = [(m.review_time - m.referral_time).days for m in meetings]
    return sum(wait_days) / len(wait_days) if wait_days else 0


def calculate_readmissions(session: Session, days: int = 30) -> int:
    admissions = session.query(Admission).order_by(Admission.patient_id, Admission.admit_time).all()
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
    appts = session.query(Appointment).all()
    total = len(appts)
    missed = sum(1 for a in appts if not a.attended or a.cancelled)
    return (missed / total) * 100 if total else 0


def calculate_bed_occupancy(session: Session, date_: datetime.date, total_beds: int = TOTAL_BEDS) -> float:
    occupied = session.query(func.count()).filter(
        Admission.admit_time <= date_,
        func.coalesce(Admission.discharge_time, date_) >= date_
    ).scalar()
    return (occupied / total_beds) * 100


def calculate_admit_to_treatment_time(session: Session) -> float:
    pairs = session.query(Admission.admit_time, Treatment.start_time).join(
        Treatment, Treatment.patient_id == Admission.patient_id
    ).filter(Treatment.start_time.isnot(None)).all()

    gaps = [(start - admit).days for admit, start in pairs if start and admit]
    return sum(gaps) / len(gaps) if gaps else 0


def aggregate_operational_metrics():
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
