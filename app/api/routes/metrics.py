
from fastapi import APIRouter
from app.services.metrics.aggregator import calculate_metrics

router = APIRouter()

@router.post("/metrics/aggregate")
def run_metrics_aggregation():
    calculate_metrics()
    return {"status": "aggregation complete"}
