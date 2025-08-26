"""Pytest fixtures and configuration for testing.

This module sets up environment variables, in-memory databases, and SQLAlchemy sessions
for running tests in isolation. It also provides lightweight factory fixtures for common
records used across the model test suite.
"""
# pylint: disable=redefined-outer-name, unused-import, import-outside-toplevel, broad-exception-caught
import os
import importlib
import uuid
from datetime import date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.database.metrics import Base
from app.models.clinician import Clinician
from app.models.treatments import Treatment, TreatmentSlotBooking

import app.config



def pytest_configure():
    """Set global pytest configuration before tests run."""
    os.environ["TESTING"] = "1"


@pytest.fixture(scope="session", autouse=True)
def load_models():
    """Ensure all models are imported to register with SQLAlchemy."""
    # Imports here to avoid circular dependency issues
    try:
        import app.models.admissions
        import app.models.appointments
        import app.models.clinician
        import app.models.metrics
        import app.models.organisation
        import app.models.pathway
        import app.models.patient
        import app.models.referrals
        import app.models.treatments
        import app.models.messaging
        import app.models.mdt
    except Exception:  # noqa: E722
        pass


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ensure SQLite enforces foreign key constraints during tests."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Automatically mock environment variables for database URIs during tests."""
    monkeypatch.setenv("PRIMARY_DB_URI", "sqlite:///./primary.db")
    monkeypatch.setenv("METRICS_DB_URI", "sqlite:///./metrics.db")
    importlib.reload(app.config)


@pytest.fixture(scope="session")
def test_engine():
    """Provide a SQLAlchemy engine connected to an in-memory SQLite database."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def test_tables(test_engine):
    """Create all tables before tests and drop them afterwards."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(test_engine, test_tables):  # pylint: disable=unused-argument
    """Provide a transactional SQLAlchemy session for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    session = session_factory()

    yield session

    session.close()
    try:
        if transaction.is_active:
            transaction.rollback()
    except InvalidRequestError:
        pass

    try:
        connection.close()
    except InvalidRequestError:
        pass


@pytest.fixture
def patient(db_session):
    """Create and persist a simple Patient record."""
    from app.models.patient import Patient  # local import keeps top-level imports tidy
    p = Patient(
        primary_guid="guid-123",
        name="Test Patient",
        admission_date=None,
        discharge_date=None,
        status="active",
    )
    db_session.add(p)
    db_session.commit()
    return p


@pytest.fixture
def clinician(db_session):
    """Provide a persisted Clinician for testing."""
    c = Clinician(
        name="Dr. Test",
        user_role="Consultant",
        primary_guid=str(uuid.uuid4()),
    )
    db_session.add(c)
    db_session.commit()
    return c


@pytest.fixture
def organisation(db_session):
    """Create and persist a simple Organisation record."""
    from app.models.organisation import Organisation
    org = Organisation(name="Test Org", code="TEST001")
    db_session.add(org)
    db_session.commit()
    return org


@pytest.fixture
def pathway_progress(db_session, patient):
    """Create and persist a simple PathwayProgress record for a patient."""
    from app.models.pathway import (
        PathwayProgress,
        PathwayStatusEnum,
        PathwayOutcomeEnum,
    )
    pp = PathwayProgress(
        patient_id=patient.id,
        status=PathwayStatusEnum.ACTIVE,
        outcome=PathwayOutcomeEnum.UNKNOWN,
        steps_total=5,
        steps_completed=0,
        readmitted=False,
        had_complication=False,
        had_relapse=False,
    )
    db_session.add(pp)
    db_session.commit()
    return pp


@pytest.fixture
def referral(db_session, patient, clinician):
    """Create referral"""
    from app.models.referrals import Referral
    r = Referral(
        patient_id=patient.id,
        clinician_id=clinician.id,
        referral_date=date.today(),
        notes="Test referral"
    )
    db_session.add(r)
    db_session.commit()
    return r


@pytest.fixture
def treatment(db_session):
    """Create and persist a Treatment record for reporting tests."""
    t = Treatment(name="Chemotherapy")
    db_session.add(t)
    db_session.commit()
    return t


@pytest.fixture
def treatment_slot_booking(db_session, treatment):
    """Create a TreatmentSlotBooking linked to a Treatment."""
    slot = TreatmentSlotBooking(
        treatment_id=treatment.id,
        patient_id=None,
        slot_time=datetime(2024, 1, 1, 10, 0)
    )
    db_session.add(slot)
    db_session.commit()
    return slot
