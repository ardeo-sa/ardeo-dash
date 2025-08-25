"""
Test suite for the patient models.
"""

from app.models.patient import Patient


def test_create_patient(db_session):
    """
    Ensure a Patient can be created and retrieved.
    """
    patient = Patient(name="Jane Doe")
    db_session.add(patient)
    db_session.commit()

    fetched = db_session.query(Patient).first()
    assert fetched.name == "Jane Doe"
