"""API endpoint to trigger metrics aggregation tasks."""
from fastapi import APIRouter
from app.services.metrics.aggregator import aggregate_operational_metrics

router = APIRouter()


@router.post("/metrics/aggregate")
def run_metrics_aggregation():
    """Trigger the aggregation of operational metrics."""
    aggregate_operational_metrics()
    return {"status": "aggregation complete"}
