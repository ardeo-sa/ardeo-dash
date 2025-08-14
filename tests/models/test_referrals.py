"""
Test suite for the referral models.
"""

from datetime import date
from app.models.referrals import Referral


def test_create_referral(db_session, patient, clinician):
    """
    Ensure a Referral can be created and retrieved.
    """
    referral = Referral(
        patient_id=patient.id,
        clinician_id=clinician.id,
        referral_date=date(2024, 1, 1),
        notes="Routine check-up"
    )
    db_session.add(referral)
    db_session.commit()

    fetched = db_session.query(Referral).first()
    assert fetched.notes == "Routine check-up"
