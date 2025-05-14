"""
API endpoint to trigger aggregation of all healthcare metrics.

This module exposes a FastAPI route that allows clients to trigger aggregation
of various metric categories including patient, MDT, pathway, and operational metrics.

The aggregated data is calculated from the primary database and persisted in
the metrics database for reporting and analysis purposes.
"""
from fastapi import APIRouter
from app.services.metrics.aggregator import aggregate_all_metrics

router = APIRouter()


@router.post("/metrics/aggregate")
def run_metrics_aggregation():
    """
    Trigger the aggregation of all healthcare-related metrics.

    This includes patient metrics, MDT metrics, pathway metrics, and operational KPIs.
    The aggregation pulls from the primary data source and saves the results
    in the metrics database.

    Returns:
        dict: A confirmation message upon successful aggregation.
    """
    aggregate_all_metrics()
    return {"status": "aggregation complete"}
