"""
Test suite for the clinician models.
"""
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.clinician import Clinician, ClinicianTask
from app.models.appointments import Appointment


def test_create_clinician(db_session, clinician):
    """
    Ensure a Clinician can be created and retrieved.
    """
    fetched = db_session.query(Clinician).first()
    assert fetched.name == clinician.name
    assert fetched.user_role ==  clinician.user_role
    assert fetched.primary_guid == clinician.primary_guid


def test_assign_task_to_clinician(db_session, clinician):
    """
    Test assigning a task to a clinician.
    """

    task = ClinicianTask(clinician_id=clinician.id, description="Review patient files")
    db_session.add(task)
    db_session.commit()

    fetched = db_session.query(Clinician).filter_by(id=clinician.id).first()
    assert len(fetched.tasks) == 1
    assert fetched.tasks[0].description == "Review patient files"


def test_clinician_appointments(db_session, patient, clinician):
    """
    Test that a clinician can have multiple appointments.
    """
    appt1 = Appointment(patient_id=patient.id, clinician_id=clinician.id, scheduled_time=datetime(2024, 8, 1, 9, 0))
    appt2 = Appointment(patient_id=patient.id, clinician_id=clinician.id, scheduled_time=datetime(2024, 8, 2, 9, 0))
    db_session.add_all([appt1, appt2])
    db_session.commit()

    fetched = db_session.query(Clinician).filter_by(id=clinician.id).first()
    assert len(fetched.appointments) == 2
    assert all(a.clinician_id == clinician.id for a in fetched.appointments)


def test_delete_clinician_removes_tasks(db_session, clinician):
    """
    Test that deleting a clinician also removes their tasks (if cascade is set).
    """
    task = ClinicianTask(clinician_id=clinician.id, description="Sign forms")
    db_session.add(task)
    db_session.commit()

    db_session.delete(clinician)
    db_session.commit()

    tasks = db_session.query(ClinicianTask).filter_by(description="Sign forms").all()
    assert tasks == []


def test_missing_required_fields_raises(db_session):
    """
    Ensure that missing required fields (name, user_role, primary_guid) raise an IntegrityError.
    """
    clinician = Clinician()  # all fields missing
    db_session.add(clinician)

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_duplicate_primary_guid_raises(db_session):
    """
    Ensure that creating two Clinicians with the same primary_guid raises an IntegrityError.
    """
    clinician1 = Clinician(name="Dr. Alpha", user_role="Surgeon", primary_guid="duplicate-guid")
    db_session.add(clinician1)
    db_session.commit()

    clinician2 = Clinician(name="Dr. Beta", user_role="Consultant", primary_guid="duplicate-guid")
    db_session.add(clinician2)

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
