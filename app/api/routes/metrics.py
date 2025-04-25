
from fastapi import APIRouter
from app.services.metrics.aggregator import aggregate_operational_metrics

router = APIRouter()

@router.post("/metrics/aggregate")
def run_metrics_aggregation():
    aggregate_operational_metrics()
    return {"status": "aggregation complete"}
