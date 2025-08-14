"""
Test suite for the treatment models.
"""

from app.models.treatments import Treatment


def test_create_treatment(db_session, patient, clinician):
    """
    Ensure a Treatment can be created and retrieved.
    """
    treatment = Treatment(
        patient_id=patient.id,
        clinician_id=clinician.id,
        description="Physical therapy session",
        status="Completed"
    )
    db_session.add(treatment)
    db_session.commit()

    fetched = db_session.query(Treatment).first()
    assert fetched.status == "Completed"
