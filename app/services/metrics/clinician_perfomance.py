"""
This module defines performance metrics for clinicians, including patient admissions,
treatment delays, readmission rates, no-show rates, patient volume, and outstanding tasks.
Each function returns a per-clinician dictionary of metric values based on data from
associated tables like admissions, pathway progress, appointments, and task assignments.
"""
from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.types import Float

from app.models.clinician import Clinician
from app.models.admission import ReferralAdmission
from app.models.pathway import PathwayProgress
from app.models.task import ClinicianTask  # assumed to track follow-ups or tasks
from app.models.attendance import Appointment  # assumed to track appointments and no-shows


def patients_admitted_per_clinician(session: Session, for_date: date = None) -> dict:
    """
    Returns the number of patients admitted per clinician on a specific date.

    Args:
        session (Session): SQLAlchemy session object.
        for_date (date, optional): The date to filter admissions. Defaults to today.

    Returns:
        dict: clinician_id -> count of admissions.
    """
    for_date = for_date or date.today()
    results = (
        session.query(
            ReferralAdmission.clinician_id,
            func.count(ReferralAdmission.id)
        )
        .filter(func.date(ReferralAdmission.admission_time) == for_date)
        .group_by(ReferralAdmission.clinician_id)
        .all()
    )
    return {clinician_id: count for clinician_id, count in results}


def avg_time_to_treatment_per_clinician(session: Session) -> dict:
    """
    Calculates average time in days from admission to treatment start for each clinician.

    Args:
        session (Session): SQLAlchemy session object.

    Returns:
        dict: clinician_id -> average duration in days.
    """
    results = (
        session.query(
            ReferralAdmission.clinician_id,
            func.avg(
                func.extract('epoch', PathwayProgress.treatment_start_time - PathwayProgress.admission_time) / 86400.0
            )
        )
        .join(PathwayProgress, ReferralAdmission.patient_id == PathwayProgress.patient_id)
        .filter(
            PathwayProgress.admission_time.isnot(None),
            PathwayProgress.treatment_start_time.isnot(None)
        )
        .group_by(ReferralAdmission.clinician_id)
        .all()
    )
    return {clinician_id: avg_days for clinician_id, avg_days in results}


def readmission_rate_per_clinician(session: Session) -> dict:
    """
    Calculates the readmission rate per clinician.

    Args:
        session (Session): SQLAlchemy session object.

    Returns:
        dict: clinician_id -> readmission rate (0–100).
    """
    results = (
        session.query(
            ReferralAdmission.clinician_id,
            func.avg(func.cast(PathwayProgress.readmitted, Float)) * 100
        )
        .join(PathwayProgress, ReferralAdmission.patient_id == PathwayProgress.patient_id)
        .group_by(ReferralAdmission.clinician_id)
        .all()
    )
    return {clinician_id: rate for clinician_id, rate in results}


def no_show_rate_per_clinician(session: Session, for_date: date = None) -> dict:
    """
    Calculates appointment no-show rate per clinician for a given day.

    Args:
        session (Session): SQLAlchemy session object.
        for_date (date, optional): Date to filter appointments. Defaults to today.

    Returns:
        dict: clinician_id -> no-show rate (0–100).
    """
    for_date = for_date or date.today()
    results = (
        session.query(
            Appointment.clinician_id,
            func.avg(func.cast(Appointment.no_show, Float)) * 100
        )
        .filter(func.date(Appointment.date) == for_date)
        .group_by(Appointment.clinician_id)
        .all()
    )
    return {clinician_id: rate for clinician_id, rate in results}


def patients_seen_per_day(session: Session, for_date: date = None) -> dict:
    """
    Returns the number of patients seen (non-no-show) by each clinician on a given day.

    Args:
        session (Session): SQLAlchemy session object.
        for_date (date, optional): The date to count patients seen. Defaults to today.

    Returns:
        dict: clinician_id -> patient count.
    """
    for_date = for_date or date.today()
    results = (
        session.query(
            Appointment.clinician_id,
            func.count(Appointment.id)
        )
        .filter(
            func.date(Appointment.date) == for_date,
            Appointment.no_show == False
        )
        .group_by(Appointment.clinician_id)
        .all()
    )
    return {clinician_id: count for clinician_id, count in results}


def outstanding_tasks_per_clinician(session: Session) -> dict:
    """
    Counts outstanding (incomplete) tasks per clinician.

    Args:
        session (Session): SQLAlchemy session object.

    Returns:
        dict: clinician_id -> count of incomplete tasks.
    """
    results = (
        session.query(
            ClinicianTask.clinician_id,
            func.count(ClinicianTask.id)
        )
        .filter(ClinicianTask.completed == False)
        .group_by(ClinicianTask.clinician_id)
        .all()
    )
    return {clinician_id: count for clinician_id, count in results}


def aggregate_clinician_metrics(session: Session, for_date: date = None) -> list[dict]:
    """
    Aggregates clinician performance metrics into a flat list of dictionaries.

    Each dictionary represents one clinician-metric pair, and contains:
    - clinician_id
    - metric_name
    - value
    - unit

    Args:
        session (Session): SQLAlchemy session.
        for_date (date, optional): Date to filter time-bound metrics. Defaults to today.

    Returns:
        list[dict]: List of aggregated clinician metrics.
    """
    for_date = for_date or date.today()

    metrics = []

    admitted = patients_admitted_per_clinician(session, for_date)
    seen = patients_seen_per_day(session, for_date)
    no_show = no_show_rate_per_clinician(session, for_date)
    time_to_treatment = avg_time_to_treatment_per_clinician(session)
    readmission = readmission_rate_per_clinician(session)
    outstanding = outstanding_tasks_per_clinician(session)

    def add_metric(metric_dict, name, unit):
        for clinician_id, value in metric_dict.items():
            metrics.append({
                "clinician_id": clinician_id,
                "metric_name": name,
                "value": value,
                "unit": unit
            })

    add_metric(admitted, "patients_admitted", "count")
    add_metric(seen, "patients_seen", "count")
    add_metric(no_show, "no_show_rate", "percent")
    add_metric(time_to_treatment, "avg_time_to_treatment", "days")
    add_metric(readmission, "readmission_rate", "percent")
    add_metric(outstanding, "outstanding_tasks", "count")

    return metrics
