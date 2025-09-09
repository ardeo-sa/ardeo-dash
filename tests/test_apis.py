"""API integration tests for messaging, metrics, and meeting services."""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.services.meeting_services import fetch_meetings


def test_run_metrics_aggregation_mocked():
    """
    API integration test for the metrics aggregation endpoint.

    This test:
    - Patches `aggregate_all_metrics` to avoid touching real databases.
    - Verifies the endpoint returns 200 and expected JSON.
    - Confirms that the aggregator function is called exactly once.
    """
    client = TestClient(app)

    with patch("app.api.routes.metrics.aggregate_all_metrics", return_value=None) as mock_aggregator:
        response = client.post("/api/metrics/aggregate")

        # Debug output (visible with pytest -s)
        print("DEBUG RESPONSE:", response.text)

        # Assert endpoint returns 200 OK
        assert response.status_code == 200
        assert response.json() == {"status": "aggregation complete"}
        mock_aggregator.assert_called_once()


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
