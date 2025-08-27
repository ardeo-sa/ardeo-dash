"""API integration tests for messaging, metrics, and meeting services."""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.services.meeting_services import fetch_meetings


def test_run_metrics_aggregation():
    """Test running the metrics aggregation endpoint with mocked aggregators."""
    from app.main import app
    from app.services.metrics import aggregator
    # from app.services.metrics.aggregator import METRIC_SOURCES

    client = TestClient(app)

    # Mock database sessions
    mock_primary = MagicMock()
    mock_primary_cm = MagicMock()
    mock_primary_cm.__enter__.return_value = mock_primary
    mock_primary_cm.__exit__.return_value = None

    mock_metrics = MagicMock()
    mock_metrics_cm = MagicMock()
    mock_metrics_cm.__enter__.return_value = mock_metrics
    mock_metrics_cm.__exit__.return_value = None

    # mock_primary.close = MagicMock()
    # mock_metrics.add = MagicMock()
    # mock_metrics.commit = MagicMock()
    # mock_metrics.rollback = MagicMock()
    # mock_metrics.close = MagicMock()


    aggregator_mocks = {
        "aggregate_operational_metrics": MagicMock(return_value={"OpMetric1": (123, "units")}),
        "aggregate_mdt_metrics": MagicMock(return_value={"meeting_count": (3, 0)}),
        "aggregate_pathway_metrics": MagicMock(return_value={"avg_admission_to_treatment_days": (5.2, 0)}),
        "aggregate_referral_metrics": MagicMock(return_value={"ReferralMetric1": (10, "referrals")}),
        "aggregate_clinician_metrics": MagicMock(return_value={"ClinicianMetric1": (5, "hrs")}),
        "aggregate_admin_metrics": MagicMock(return_value={"AdminMetric1": (2, "actions")}),
    }

    model_mocks = {
        "OperationalMetrics": MagicMock(),
        "MDTMetrics": MagicMock(),
        "PathwayMetrics": MagicMock(),
        "ReferralMetrics": MagicMock(),
        "ClinicianMetrics": MagicMock(),
        "AdminMetrics": MagicMock(),
    }

    with patch.multiple(
            "app.services.metrics.aggregator",
            init_metrics_engine=MagicMock(),
            PrimarySessionLocal=MagicMock(return_value=mock_primary_cm),
            MetricsSessionLocal=MagicMock(return_value=mock_metrics_cm),
            **aggregator_mocks,
            **model_mocks
    ):

        response = client.post("/api/metrics/aggregate")
        print("DEBUG RESPONSE:", response.text)

        assert response.status_code in (200, 204)

        # Check that metrics were added
        added_metrics = [call[0][0] for call in mock_metrics.add.call_args_list]
        metric_type_names = [metric.__class__.__name__ for metric in added_metrics]

        assert "OperationalMetrics" in metric_type_names
        assert "MDTMetrics" in metric_type_names
        assert "PathwayMetrics" in metric_type_names
        assert "ReferralMetrics" in metric_type_names
        assert "ClinicianMetrics" in metric_type_names
        assert "AdminMetrics" in metric_type_names

        # for name in model_mocks.keys():
        #     assert name in metric_type_names

@patch("app.services.meeting_services.requests.get")
def test_fetch_meetings_mocked(mock_requests_get):
    """Test fetching meetings with requests.get mocked."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": "mocked-id", "timestamp": "2024-06-26T12:00:00Z", "read": False}
    ]
    mock_requests_get.return_value = mock_response

    result = fetch_meetings()
    assert isinstance(result, list)
    assert result[0]["id"] == "mocked-id"
