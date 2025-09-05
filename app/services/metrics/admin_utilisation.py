"""
This module defines metrics for administrative and resource utilization, including:
- Patient-to-clinician ratios
- Use of diagnostics and treatment slots
"""
import logging
from datetime import datetime, date
from typing import Dict, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.reporting.admissions import ReferralAdmission as Admission
from app.models.reporting.clinician import Clinician

from app.models.reporting.imaging import ImagingOrder
from app.models.reporting.lab import LabTestOrder
from app.models.reporting.treatments import TreatmentSlotBooking

logger = logging.getLogger(__name__)

def calculate_patient_to_clinician_ratio(session: Session, for_date: date = None) -> float:
    """
    Calculates the average number of patients per clinician for a given day.

    Args:
        session (Session): SQLAlchemy session.
        for_date (date): Optional date filter (defaults to today).

    Returns:
        float: Ratio of patients to clinicians.
    """
    for_date = for_date or date.today()
    patient_count = session.query(Admission).filter(func.date(Admission.admission_time) == for_date).count()
    clinician_count = session.query(Clinician).count()
    ratio = (patient_count / clinician_count) if clinician_count else 0
    logger.debug(
        "Patient-to-clinician ratio for %s: %s patients, %s clinicians => ratio = %.2f",
        for_date, patient_count, clinician_count, ratio
    )
    return ratio


def calculate_imaging_utilization(session: Session, for_date: date = None) -> int:
    """
    Counts imaging procedures ordered on a given day.

    Returns:
        int: Number of imaging orders.
    """
    for_date = for_date or date.today()
    count = session.query(ImagingOrder).filter(func.date(ImagingOrder.created_at) == for_date).count()
    logger.debug("Imaging utilization for %s: %d", for_date, count)
    return count


def calculate_lab_test_utilization(session: Session, for_date: date = None) -> int:
    """
    Counts lab tests ordered on a given day.

    Returns:
        int: Number of lab test orders.
    """
    for_date = for_date or date.today()
    count = session.query(LabTestOrder).filter(func.date(LabTestOrder.created_at) == for_date).count()
    logger.debug("Lab test utilization for %s: %d", for_date, count)
    return count


def calculate_treatment_slot_utilization(session: Session, for_date: date = None) -> int:
    """
    Counts booked treatment slots on a given day.

    Returns:
        int: Number of booked treatment slots.
    """
    for_date = for_date or date.today()
    count = session.query(TreatmentSlotBooking).filter(
        func.date(TreatmentSlotBooking.slot_time) == for_date
    ).count()
    logger.debug("Treatment slot utilization for %s: %d", for_date, count)
    return count


def aggregate_admin_metrics(session: Session, date_: date = None) -> Dict[str, Tuple[float, str]]:
    """
    Aggregates key administrative and resource utilization metrics for a given day,
    returning values with their units.

    Args:
        session (Session): SQLAlchemy session to query the database.
        date_ (date, optional): Date for which metrics should be calculated. Defaults to today.

    Returns:
        Dict[str, Tuple[float, str]]: Dictionary with metric names as keys and (value, unit) tuples as values.
    """
    date_ = date_ or datetime.today().date()
    logger.info("Aggregating admin metrics for date: %s", date_)

    metrics: Dict[str, Tuple[float, str]] = {
        "patient_to_clinician_ratio": (calculate_patient_to_clinician_ratio(session, date_), "ratio"),
        "imaging_utilization": (calculate_imaging_utilization(session, date_), "percent"),
        "lab_test_utilization": (calculate_lab_test_utilization(session, date_), "percent"),
        "treatment_slot_utilization": (calculate_treatment_slot_utilization(session, date_), "percent"),
    }

    logger.debug("Aggregated admin metrics with units: %s", metrics)
    return metrics
