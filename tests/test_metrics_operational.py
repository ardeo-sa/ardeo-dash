import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from app.services.metrics.operational import (
    get_admissions_discharge_counts,
    calculate_avg_length_of_stay,
    calculate_readmissions,
)
from app.models.admission import Admission


def make_admission(patient_id, admit_days_ago, discharge_days_ago=None):
    admit_time = datetime.now() - timedelta(days=admit_days_ago)
    discharge_time = None
    if discharge_days_ago is not None:
        discharge_time = datetime.now() - timedelta(days=discharge_days_ago)
    return Admission(patient_id=patient_id, admit_time=admit_time, discharge_time=discharge_time)


def test_avg_length_of_stay():
    mock_session = MagicMock()
    mock_admissions = [
        make_admission(1, 10, 5),
        make_admission(2, 8, 2),
        make_admission(3, 6, 1)
    ]
    mock_session.query.return_value.filter.return_value.all.return_value = mock_admissions

    from app.services.metrics.operational import calculate_avg_length_of_stay
    result = calculate_avg_length_of_stay(mock_session)
    assert round(result, 1) == 4.0


def test_readmission_count():
    mock_session = MagicMock()
    now = datetime.now()
    mock_admissions = [
        Admission(patient_id=1, admit_time=now - timedelta(days=60), discharge_time=now - timedelta(days=50)),
        Admission(patient_id=1, admit_time=now - timedelta(days=20), discharge_time=now - timedelta(days=10)),  # readmission
        Admission(patient_id=2, admit_time=now - timedelta(days=15), discharge_time=now - timedelta(days=5)),
    ]
    mock_session.query.return_value.order_by.return_value.all.return_value = mock_admissions

    result = calculate_readmissions(mock_session)
    assert result == 1


def test_get_admissions_discharge_counts():
    mock_session = MagicMock()
    test_date = datetime.today().date()
    mock_session.query.return_value.filter.return_value.scalar.side_effect = [3, 2]

    adm, dis = get_admissions_discharge_counts(mock_session, test_date)
    assert adm == 3
    assert dis == 2
