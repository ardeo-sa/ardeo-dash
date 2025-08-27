"""
Test suite for the treatment models.
"""
from app.models.treatments import Treatment, TreatmentSlotBooking


def test_retrieve_treatment(db_session, treatment):
    """Ensure a Treatment can be retrieved."""
    fetched = db_session.query(Treatment).first()
    assert fetched.name == "Chemotherapy"

def test_retrieve_treatment_slot_booking(db_session, treatment_slot_booking):
    """Ensure a TreatmentSlotBooking can be retrieved and linked to a Treatment."""
    fetched = db_session.query(TreatmentSlotBooking).first()
    assert fetched.treatment_id == fetched.treatment.id
    assert fetched.slot_time.hour == 10
