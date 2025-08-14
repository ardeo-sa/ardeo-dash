"""API integration tests for messaging, metrics, and meeting services."""

from uuid import uuid4
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.services.meeting_services import fetch_meetings

client = TestClient(app)

# Sample message payload for messaging API tests
message_input = {
    "conversation_id": str(uuid4()),
    "sender_id": str(uuid4()),
    "receiver_id": str(uuid4()),
    "content": "Hello, this is a test message"
}


@patch("app.api.routes.messaging.create_message")
def test_send_message(mock_create_message):
    """Test sending a message through the messaging API."""
    mock_create_message.return_value = {
        "id": str(uuid4()),
        "timestamp": "2024-06-19T12:00:00Z",
        "read": False
    }
    response = client.post("/api/messages/", json=message_input)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "timestamp" in data
    assert data["read"] is False


@patch("app.api.routes.messaging.get_conversation_messages")
def test_fetch_messages_success(mock_get_messages):
    """Test retrieving messages for a given conversation ID."""
    conversation_id = str(uuid4())
    mock_get_messages.return_value = [
        {
            "id": str(uuid4()),
            "timestamp": "2024-06-19T12:00:00Z",
            "read": False
        },
        {
            "id": str(uuid4()),
            "timestamp": "2024-06-19T12:01:00Z",
            "read": True
        }
    ]

    response = client.get(f"/api/messages/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "id" in data[0]
    assert "timestamp" in data[0]
    assert "read" in data[0]


# pylint: disable=too-many-arguments,too-many-positional-arguments
@patch("app.services.metrics.aggregator.aggregate_admin_metrics")
@patch("app.services.metrics.aggregator.aggregate_clinician_metrics")
@patch("app.services.metrics.aggregator.aggregate_referral_metrics")
@patch("app.services.metrics.aggregator.aggregate_pathway_metrics")
@patch("app.services.metrics.aggregator.aggregate_mdt_metrics")
@patch("app.services.metrics.aggregator.aggregate_operational_metrics")
@patch("app.services.metrics.aggregator.PrimarySessionLocal")
@patch("app.services.metrics.aggregator.MetricsSessionLocal")
@patch("app.services.metrics.aggregator.init_metrics_db")
def test_run_metrics_aggregation(
    mock_init_metrics_db,  # pylint: disable=unused-argument
    mock_metrics_session,
    mock_primary_session,
    mock_operational_metrics,
    mock_mdt_metrics,
    mock_pathway_metrics,
    mock_referral_metrics,
    mock_clinician_metrics,
    mock_admin_metrics
):
    """Test running the metrics aggregation endpoint with mocked aggregators."""
    mock_operational_metrics.return_value = {
        "OpMetric1": (123, "units")
    }
    mock_mdt_metrics.return_value = {
        "meeting_count": (3, 0),
        "avg_attendance": (85.5, 0),
        "avg_wait_time": (1.2, 0),
        "action_completion_rate": (90.0, 0)
    }
    mock_pathway_metrics.return_value = {
        "avg_admission_to_treatment_days": (5.2, 0),
        "readmission_rate_30d": (8.5, 0),
        "no_show_rate": (3.4, 0)
    }
    mock_referral_metrics.return_value = {
        "ReferralMetric1": (10, "referrals")
    }
    mock_clinician_metrics.return_value = {
        "ClinicianMetric1": (5, "hrs")
    }
    mock_admin_metrics.return_value = {
        "AdminMetric1": (2, "actions")
    }

    mock_primary = MagicMock()
    mock_metrics = MagicMock()
    mock_primary_session.return_value.__enter__.return_value = mock_primary
    mock_metrics_session.return_value.__enter__.return_value = mock_metrics

    response = client.post("/api/metrics/aggregate")
    assert response.status_code in (200, 204)

    added_metrics = [call[0][0] for call in mock_metrics.add.call_args_list]
    metric_type_names = [metric.__class__.__name__ for metric in added_metrics]
    assert "OperationalMetrics" in metric_type_names
    assert "MDTMetrics" in metric_type_names
    assert "PathwayMetrics" in metric_type_names
    assert "ReferralMetrics" in metric_type_names
    assert "ClinicianMetrics" in metric_type_names
    assert "AdminMetrics" in metric_type_names


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
