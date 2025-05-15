"""
This module defines a Celery task for aggregating operational metrics.

The `run_metric_aggregation` function is a Celery task that, when triggered,
invokes the `calculate_metrics()` function from the `app.services.metrics.aggregator`
module to aggregate and store operational metrics in the system.

The task runs asynchronously in the background, allowing the system to process metric aggregation
without blocking other operations.

Modules:
    - `calculate_metrics`: A function that performs the aggregation of metrics.
    - `celery`: The Celery instance used to define and execute the task.

Usage:
    To execute the metric aggregation asynchronously, call the `run_metric_aggregation` task
    within the Celery worker framework.
"""
from .worker import celery
from app.services.metrics.aggregator import calculate_metrics

@celery.task
def run_metric_aggregation():
    """
        Celery task that triggers the aggregation of operational metrics.

        This task calls the `calculate_metrics()` function to aggregate and store
        the operational metrics for the system. It runs asynchronously as a background task.

        Args:
            None

        Returns:
            None
        """
    calculate_metrics()
