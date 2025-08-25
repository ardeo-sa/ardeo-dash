"""
This module defines a Celery task for aggregating operational metrics.

The `run_metric_aggregation` function is a Celery task that, when triggered,
invokes the `calculate_metrics()` function from the `app.services.metrics.aggregator`
module to aggregate and store operational metrics in the system.

The task runs asynchronously in the background, allowing the system to process metric aggregation
without blocking other data_processing.

Modules:
    - `calculate_metrics`: A function that performs the aggregation of metrics.
    - `celery`: The Celery instance used to define and execute the task.

Usage:
    To execute the metric aggregation asynchronously, call the `run_metric_aggregation` task
    within the Celery worker framework.
"""
import logging

from app.services.metrics.aggregator import aggregate_all_metrics
from app.tasks.worker import celery

logger = logging.getLogger(__name__)

@celery.task(name="run_metric_aggregation")
def run_metric_aggregation_task():
    """
        Celery task that triggers the aggregation of operational metrics.

        This task calls the `calculate_metrics()` function to aggregate and store
        the operational metrics for the system. It runs asynchronously as a background task.

        Args:
            None

        Returns:
            None
        """
    logger.info("Starting metrics aggregation task.")
    aggregate_all_metrics()
    logger.info("Metrics aggregation task completed.")
