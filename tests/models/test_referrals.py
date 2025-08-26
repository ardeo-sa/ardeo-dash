"""
Test suite for the referral models.
"""
from app.models.referrals import Referral


def test_retrieve_referral(db_session, referral):
    """
    Ensure a Referral can be retrieved and its fields are correct.
    """
    fetched = db_session.query(Referral).filter_by(id=referral.id).first()

    assert fetched is not None
    assert fetched.patient_id == referral.patient_id
    assert fetched.clinician_id == referral.clinician_id
    assert fetched.referral_date == referral.referral_date
    assert fetched.notes == referral.notes
