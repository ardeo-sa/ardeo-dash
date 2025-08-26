"""
Test suite for the patient models.
"""

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.patient import Patient


def test_retrieve_patient(db_session, patient):
    """
    Ensure that a Patient can be retrieved from the database and its fields are correct.
    """
    fetched = db_session.query(Patient).filter_by(id=patient.id).first()

    assert fetched is not None
    assert fetched.primary_guid == patient.primary_guid
    assert fetched.name == patient.name
    assert fetched.status == patient.status
    assert fetched.admission_date == patient.admission_date
    assert fetched.discharge_date == patient.discharge_date


def test_patient_missing_required_fields_raises(db_session):
    """
    Ensure that creating a Patient without required fields raises IntegrityError.
    """
    # primary_guid is required
    incomplete_patient = Patient(name="John Doe")
    db_session.add(incomplete_patient)

    with pytest.raises(IntegrityError):
        db_session.commit()
