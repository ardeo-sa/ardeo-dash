"""
This module defines performance metrics for clinicians, including patient admissions,
patient volume, and outstanding tasks.
Each function returns a per-clinician dictionary of metric values based on data from
associated tables like admissions, pathway progress, appointments, and task assignments.
"""
from datetime import date, datetime
from typing import Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.types import Float

from app.models.clinician import Clinician
from app.models.admissions import ReferralAdmission
from app.models.pathway import PathwayProgress
from app.models.clinician import ClinicianTask
from app.models.appointments import Appointment


def get_active_clinician_count(session: Session, for_date: date) -> int:
    """
    Returns the count of clinicians who were active (had an admission, appointment, or task)
    on the given day.

    Args:
        session (Session): SQLAlchemy session.
        for_date (date): Date to evaluate activity.

    Returns:
        int: Number of distinct active clinicians.
    """
    admission_ids = session.query(ReferralAdmission.clinician_id).filter(
        func.date(ReferralAdmission.admission_time) == for_date
    )

    appointment_ids = session.query(Appointment.clinician_id).filter(
        func.date(Appointment.date) == for_date
    )

    task_ids = session.query(ClinicianTask.clinician_id).filter(
        func.date(ClinicianTask.created_at) == for_date  # adjust field if different
    )

    active_ids = admission_ids.union(appointment_ids).union(task_ids).distinct()
    return active_ids.count()


def avg_patients_admitted(session: Session, for_date: date, clinician_count: int) -> float:
    total = session.query(ReferralAdmission).filter(
        func.date(ReferralAdmission.admission_time) == for_date
    ).count()
    return total / clinician_count if clinician_count else 0


def avg_patients_seen(session: Session, for_date: date, clinician_count: int) -> float:
    total = session.query(Appointment).filter(
        func.date(Appointment.date) == for_date,
        Appointment.no_show == False
    ).count()
    return total / clinician_count if clinician_count else 0


def avg_outstanding_tasks(session: Session, clinician_count: int) -> float:
    total = session.query(ClinicianTask).filter(
        ClinicianTask.completed == False
    ).count()
    return total / clinician_count if clinician_count else 0


def aggregate_clinician_metrics(session: Session, date_: date = None) -> Dict[str, Any]:
    """
    Aggregates system-level clinician metrics averaged per active clinician.

    Args:
        session (Session): SQLAlchemy session.
        date_ (date, optional): Date to calculate metrics for. Defaults to today.

    Returns:
        Dict[str, Any]: Dictionary of metric_name -> value.
    """
    date_ = date_ or datetime.today().date()
    clinician_count = get_active_clinician_count(session, date_)

    return {
        "date": date_,
        "active_clinicians": clinician_count,
        "avg_patients_admitted": avg_patients_admitted(session, date_, clinician_count),
        "avg_patients_seen": avg_patients_seen(session, date_, clinician_count),
        "avg_outstanding_tasks": avg_outstanding_tasks(session, clinician_count),
    }
