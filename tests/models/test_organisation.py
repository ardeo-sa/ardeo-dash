"""
Test suite for the organisation models.
"""
import pytest
from app.models.organisation import Organisation


def test_retrieve_organisation(db_session):
    """
    Ensure an Organisation can be created and retrieved successfully.
    """
    org = Organisation(name="Test Hospital", code="TH001")
    db_session.add(org)
    db_session.commit()

    fetched = db_session.query(Organisation).first()
    assert fetched.name == "Test Hospital"
    assert fetched.code == "TH001"
