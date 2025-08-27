"""
Comprehensive test suite for metrics models.
Covers: OperationalMetrics, MDTMetrics, PathwayMetrics, ReferralMetrics, ClinicianMetrics, AdminMetrics
"""

import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from app.models.metrics import (
    OperationalMetrics,
    MDTMetrics,
    PathwayMetrics,
    ReferralMetrics,
    ClinicianMetrics,
    AdminMetrics,
)


def test_create_operational_metric(db_session):
    """
    Test that an OperationalMetrics record can be created and retrieved.
    """
    metric = OperationalMetrics(
        date=date.today(),
        metric_name="Avg LOS",
        value=5.2,
        unit="days"
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(OperationalMetrics).first()
    assert fetched.metric_name == "Avg LOS"
    assert fetched.unit == "days"


def test_create_mdt_metric(db_session):
    """
    Test that an MDTMetrics record can be created and retrieved.
    """
    metric = MDTMetrics(
        date=date.today(),
        metric_name="MDT Attendance",
        meeting_count=3,
        avg_attendance=85.0,
        avg_wait_time=2.0,
        action_completion_rate=90.0
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(MDTMetrics).first()
    assert fetched.meeting_count == 3
    assert fetched.avg_attendance == 85.0


def test_create_pathway_metric(db_session):
    """
    Test that a PathwayMetrics record can be created and retrieved.
    """
    metric = PathwayMetrics(
        date=date.today(),
        metric_name="Readmission Rate",
        avg_admission_to_treatment_days=4.5,
        readmission_rate_30d=12.5,
        no_show_rate=5.0
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(PathwayMetrics).first()
    assert fetched.readmission_rate_30d == 12.5


def test_create_referral_metric(db_session):
    """
    Test that a ReferralMetrics record can be created and retrieved.
    """
    metric = ReferralMetrics(
        date=date.today(),
        metric_name="Conversion Rate",
        value=25.0,
        unit="percent"
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(ReferralMetrics).first()
    assert fetched.value == 25.0
    assert fetched.unit == "percent"


def test_create_clinician_metric(db_session):
    """
    Test that a ClinicianMetrics record can be created and retrieved.
    """
    metric = ClinicianMetrics(
        date=date.today(),
        metric_name="Patients Seen",
        value=10,
        unit="count"
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(ClinicianMetrics).first()
    assert fetched.value == 10


def test_create_admin_metric(db_session):
    """
    Test that an AdminMetrics record can be created and retrieved.
    """
    metric = AdminMetrics(
        date=date.today(),
        metric_name="Patient to Clinician Ratio",
        value=4.5,
        unit="ratio"
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(AdminMetrics).first()
    assert fetched.metric_name == "Patient to Clinician Ratio"


@pytest.mark.parametrize(
    "MetricClass, required_fields",
    [
        (OperationalMetrics, {"date": date.today(), "metric_name": "Avg LOS", "value": 5.0, "unit": "days"}),
        (MDTMetrics, {"date": date.today(), "metric_name": "MDT Attendance", "meeting_count": 3, "avg_attendance": 80.0, "avg_wait_time": 1.0, "action_completion_rate": 90.0}),
        (PathwayMetrics, {"date": date.today(), "metric_name": "Readmission Rate", "avg_admission_to_treatment_days": 4.5, "readmission_rate_30d": 10.0, "no_show_rate": 5.0}),
        (ReferralMetrics, {"date": date.today(), "metric_name": "Conversion Rate", "value": 25.0, "unit": "percent"}),
        (ClinicianMetrics, {"date": date.today(), "metric_name": "Patients Seen", "value": 10, "unit": "count"}),
        (AdminMetrics, {"date": date.today(), "metric_name": "Patient to Clinician Ratio", "value": 4.5, "unit": "ratio"}),
    ]
)
def test_metrics_missing_required_fields(db_session, MetricClass, required_fields):
    # Remove one required field at a time to ensure IntegrityError
    for field in required_fields.keys():
        data = required_fields.copy()
        data.pop(field)
        metric = MetricClass(**data)
        db_session.add(metric)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()



@pytest.mark.parametrize(
    "MetricClass, initial_data, updated_value, update_field",
    [
        (OperationalMetrics, {"date": date.today(), "metric_name": "Avg LOS", "value": 5.2, "unit": "days"}, 6.0, "value"),
        (MDTMetrics, {"date": date.today(), "metric_name": "MDT Attendance", "meeting_count": 3, "avg_attendance": 80.0, "avg_wait_time": 1.0, "action_completion_rate": 90.0}, 85.0, "avg_attendance"),
        (PathwayMetrics, {"date": date.today(), "metric_name": "Readmission Rate", "avg_admission_to_treatment_days": 4.5, "readmission_rate_30d": 10.0, "no_show_rate": 5.0}, 12.0, "readmission_rate_30d"),
        (ReferralMetrics, {"date": date.today(), "metric_name": "Conversion Rate", "value": 25.0, "unit": "percent"}, 30.0, "value"),
        (ClinicianMetrics, {"date": date.today(), "metric_name": "Patients Seen", "value": 10, "unit": "count"}, 15, "value"),
        (AdminMetrics, {"date": date.today(), "metric_name": "Patient to Clinician Ratio", "value": 4.5, "unit": "ratio"}, 5.0, "value"),
    ]
)
def test_metrics_update(db_session, MetricClass, initial_data, updated_value, update_field):
    metric = MetricClass(**initial_data)
    db_session.add(metric)
    db_session.commit()

    setattr(metric, update_field, updated_value)
    db_session.commit()

    fetched = db_session.query(MetricClass).first()
    assert getattr(fetched, update_field) == updated_value
