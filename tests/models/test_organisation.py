"""
Test suite for the organisation models.
"""

from app.models.organisation import Organisation


def test_create_organisation(db_session):
    """
    Ensure an Organisation can be created and retrieved.
    """
    org = Organisation(name="Test Hospital")
    db_session.add(org)
    db_session.commit()

    fetched = db_session.query(Organisation).first()
    assert fetched.name == "Test Hospital"
