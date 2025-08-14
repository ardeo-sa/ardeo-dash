"""
Test suite for the metrics models.
"""

from app.models.metrics import OperationalMetrics


def test_create_operational_metric(db_session):
    """
    Ensure an OperationalMetric can be created and retrieved.
    """
    metric = OperationalMetrics(
        name="Avg LOS",
        value=5.2,
        unit="days"
    )
    db_session.add(metric)
    db_session.commit()

    fetched = db_session.query(OperationalMetrics).first()
    assert fetched.name == "Avg LOS"
    assert fetched.unit == "days"
