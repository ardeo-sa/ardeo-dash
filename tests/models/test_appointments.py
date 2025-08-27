"""
Test suite for the appointment models.
"""

from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.appointments import Appointment


def test_create_appointment(db_session, patient, clinician):
    """
    Ensure that an Appointment can be created and retrieved.
    """
    appointment = Appointment(
        patient_id=patient.id,
        clinician_id=clinician.id,
        scheduled_time=datetime(2024, 1, 1, 9, 0),
        attended=True,
        cancelled=False,
    )
    db_session.add(appointment)
    db_session.commit()

    fetched = db_session.query(Appointment).first()
    assert fetched.attended is True
    assert fetched.cancelled is False
    assert fetched.clinician.name == clinician.name


def test_appointment_missing_required_fields(db_session, patient, clinician):
    """
    Ensure that missing required fields raises an IntegrityError.
    """
    appointment = Appointment(patient_id=patient.id, clinician_id=clinician.id)
    db_session.add(appointment)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_appointment_invalid_foreign_keys(db_session):
    """
    Ensure that using invalid patient_id or clinician_id raises an IntegrityError.
    """
    appointment = Appointment(
        patient_id=9999,
        clinician_id=9999,
        scheduled_time=datetime(2024, 1, 1, 9, 0)
    )
    db_session.add(appointment)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
