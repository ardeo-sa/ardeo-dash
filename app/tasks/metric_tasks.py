
from app.services.aggregations import calculate_metrics
from .worker import celery

@celery.task
def run_metric_aggregation():
    calculate_metrics()
