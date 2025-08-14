"""
Test suite for the clinician models.
"""

from app.models.clinician import Clinician

def test_create_clinician(db_session):
    """
    Ensure a Clinician can be created and retrieved.
    """
    clinician = Clinician(name="Dr. House", role="Consultant")
    db_session.add(clinician)
    db_session.commit()

    fetched = db_session.query(Clinician).first()
    assert fetched.name == "Dr. House"
    assert fetched.role == "Consultant"
