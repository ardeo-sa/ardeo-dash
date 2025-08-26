"""
Test suite for the admissions models.

This module contains unit tests for:
- ReferralAdmission
- ReferralStatusEnum
"""

from datetime import datetime, date
import pytest
from sqlalchemy.exc import IntegrityError
from app.models.admissions import ReferralAdmission, ReferralStatusEnum


def test_enum_values():
    """
    Ensure ReferralStatusEnum contains all expected values.
    """
    expected = {
        "Pending",
        "Referred In",
        "Referred Out",
        "Discharged",
        "Completed",
        "Cancelled",
    }
    assert {e.value for e in ReferralStatusEnum} == expected


def test_create_referral_admission(db_session, patient, clinician, organisation, pathway_progress):
    """
    Test that a ReferralAdmission can be created and retrieved from the database.
    """
    referral = ReferralAdmission(
        admit_time=datetime(2024, 1, 1, 10, 0),
        discharge_time=datetime(2024, 1, 5, 15, 0),
        patient_id=patient.id,
        referral_date=date(2024, 1, 1),
        discharge_date=date(2024, 1, 5),
        referral_type="In",
        referring_clinician_id=clinician.id,
        receiving_clinician_id=clinician.id,
        receiving_organisation_id=organisation.id,
        pathway_id=pathway_progress.id,
        discharge_notes="Patient recovered well.",
    )
    db_session.add(referral)
    db_session.commit()

    fetched = db_session.query(ReferralAdmission).first()
    assert fetched.referral_status == ReferralStatusEnum.PENDING
    assert fetched.receiving_clinician.name == clinician.name


def test_missing_required_fields_raises(db_session):
    """
    Test that creating a ReferralAdmission without required fields raises IntegrityError.
    """
    with pytest.raises(IntegrityError):
        db_session.add(ReferralAdmission(referral_type="Out"))
        db_session.commit()
