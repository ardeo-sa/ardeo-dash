"""
Test suite for the appointment models.
"""

from datetime import datetime
from app.models.appointments import Appointment


def test_create_appointment(db_session, patient, clinician):
    """
    Ensure that an Appointment can be created and retrieved.
    """
    appointment = Appointment(
        patient_id=patient.id,
        clinician_id=clinician.id,
        scheduled_time=datetime(2024, 1, 1, 9, 0),
        status="Scheduled",
    )
    db_session.add(appointment)
    db_session.commit()

    fetched = db_session.query(Appointment).first()
    assert fetched.status == "Scheduled"
    assert fetched.clinician.name == clinician.name
