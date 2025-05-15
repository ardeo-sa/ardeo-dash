"""
This module defines metrics for administrative and resource utilization, including:
- Patient-to-clinician ratios
- Use of diagnostics and treatment slots
"""
from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.admission import Admission
from app.models.clinician import Clinician

# These models should exist in your system or be replaced with appropriate ones
from app.models.imaging import ImagingOrder
from app.models.lab import LabTestOrder
from app.models.treatments import TreatmentSlotBooking


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
    return (patient_count / clinician_count) if clinician_count else 0


def calculate_imaging_utilization(session: Session, for_date: date = None) -> int:
    """
    Counts imaging procedures ordered on a given day.

    Returns:
        int: Number of imaging orders.
    """
    for_date = for_date or date.today()
    return session.query(ImagingOrder).filter(func.date(ImagingOrder.created_at) == for_date).count()


def calculate_lab_test_utilization(session: Session, for_date: date = None) -> int:
    """
    Counts lab tests ordered on a given day.

    Returns:
        int: Number of lab test orders.
    """
    for_date = for_date or date.today()
    return session.query(LabTestOrder).filter(func.date(LabTestOrder.created_at) == for_date).count()


def calculate_treatment_slot_utilization(session: Session, for_date: date = None) -> int:
    """
    Counts booked treatment slots on a given day.

    Returns:
        int: Number of booked treatment slots.
    """
    for_date = for_date or date.today()
    return session.query(TreatmentSlotBooking).filter(
        func.date(TreatmentSlotBooking.slot_time) == for_date
    ).count()
