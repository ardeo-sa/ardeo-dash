"""
Test the operational metrics aggregation functions, including:
- Average Length of Stay (LOS)
- Readmission Count
- Admission and Discharge Counts

These tests mock the database session and query results to ensure correct
functionality of the metrics calculations without requiring actual database access.

Functions:
    - make_admission: Helper function to create mock `ReferralAdmission`
      instances with specified admit and discharge times.
    - test_avg_length_of_stay: Test the `calculate_avg_length_of_stay`
      function to ensure it calculates the average length of stay correctly.
    - test_readmission_count: Test the `calculate_readmissions` function
      to ensure it counts readmissions correctly.
    - test_get_admissions_discharge_counts: Test the `get_admissions_discharge_counts`
      function to verify the correct counts of admissions and discharges.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from app.services.metrics.operational import (
    get_admissions_discharge_counts,
    calculate_avg_length_of_stay,
    calculate_readmissions,
)
from app.models.admissions import ReferralAdmission
from app.models.patient import Patient
from app.models.clinician import Clinician
from app.models.treatments import Treatment

def make_admission(patient_id, admit_days_ago, discharge_days_ago=None):
    """
        Creates a mock ReferralAdmission instance with specified admission and discharge times.

        Args:
            patient_id (int): The ID of the patient.
            admit_days_ago (int): The number of days ago the admission occurred.
            discharge_days_ago (int, optional): The number of days ago the discharge occurred. Defaults to None.

        Returns:
            ReferralAdmission: The mock ReferralAdmission instance.
    """
    admit_time = datetime.now() - timedelta(days=admit_days_ago)
    discharge_time = None
    if discharge_days_ago is not None:
        discharge_time = datetime.now() - timedelta(days=discharge_days_ago)
    return ReferralAdmission(patient_id=patient_id, admit_time=admit_time, discharge_time=discharge_time)

def test_avg_length_of_stay():
    """
        Tests the `calculate_avg_length_of_stay` function to ensure it calculates
        the correct average length of stay from a mock session.

        This test verifies that the function correctly calculates the average
        length of stay based on mock data with different admission and discharge
        times.

        Asserts:
            - The calculated average length of stay is approximately 5.3 days.
    """
    mock_session = MagicMock()
    mock_admissions = [
        make_admission(1, 10, 5),
        make_admission(2, 8, 2),
        make_admission(3, 6, 1)
    ]
    mock_session.query.return_value.filter.return_value.all.return_value = mock_admissions

    from app.services.metrics.operational import calculate_avg_length_of_stay
    result = calculate_avg_length_of_stay(mock_session)
    assert round(result, 1) == 5.3

def test_readmission_count():
    """
        Tests the `calculate_readmissions` function to verify it correctly counts
        the number of readmissions based on the mock session.

        This test ensures that the function counts readmissions correctly, considering
        admissions within 30 days of a previous discharge.

        Asserts:
            - The readmission count is correctly calculated as 1.
    """
    mock_session = MagicMock()
    now = datetime.now()
    mock_admissions = [
        ReferralAdmission(patient_id=1, admit_time=now - timedelta(days=60), discharge_time=now - timedelta(days=50)),
        ReferralAdmission(patient_id=1, admit_time=now - timedelta(days=20), discharge_time=now - timedelta(days=10)),  # readmission
        ReferralAdmission(patient_id=2, admit_time=now - timedelta(days=15), discharge_time=now - timedelta(days=5)),
    ]
    mock_session.query.return_value.order_by.return_value.all.return_value = mock_admissions

    result = calculate_readmissions(mock_session)
    assert result == 1


def test_get_admissions_discharge_counts():
    """
        Tests the `get_admissions_discharge_counts` function to ensure it returns
        the correct counts for admissions and discharges for a given date.

        This test checks that the function correctly retrieves the number of admissions
        and discharges based on the mock session and given date.

        Asserts:
            - The admission count is 3.
            - The discharge count is 2.
    """
    mock_session = MagicMock()
    test_date = datetime.today().date()
    mock_session.query.return_value.filter.return_value.scalar.side_effect = [3, 2]

    adm, dis = get_admissions_discharge_counts(mock_session, test_date)
    assert adm == 3
    assert dis == 2
