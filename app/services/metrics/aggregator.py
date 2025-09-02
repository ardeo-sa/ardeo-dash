"""
This module aggregates various types of metrics from the primary database and stores them in the metrics database.

Functions:
- `aggregate_all_metrics`: The main entry point for aggregating and saving all metrics.
"""
import logging
from datetime import date

from app.database.primary import PRIMARY_SESSION_LOCAL as PrimarySessionLocal
from app.database.metrics import MetricsSessionLocal, init_metrics_engine
from app.models.reporting.metrics import (
    PathwayMetrics,
    OperationalMetrics,
    MDTMetrics,
    ReferralMetrics,
    ClinicianMetrics,
    AdminMetrics,
)
from app.services.metrics.pathway import aggregate_pathway_metrics
from app.services.metrics.operational import aggregate_operational_metrics
from app.services.metrics.mdt import aggregate_mdt_metrics
from app.services.metrics.referrals import aggregate_referral_metrics
from app.services.metrics.clinician_performance import aggregate_clinician_metrics
from app.services.metrics.admin_utilisation import aggregate_admin_metrics

logger = logging.getLogger(__name__)

# Map category → (aggregator_function, ORM model)
METRIC_SOURCES = {
    "operational": (aggregate_operational_metrics, OperationalMetrics),
    "mdt":         (aggregate_mdt_metrics, MDTMetrics),
    "pathway":     (aggregate_pathway_metrics, PathwayMetrics),
    "referral":    (aggregate_referral_metrics, ReferralMetrics),
    "clinician":   (aggregate_clinician_metrics, ClinicianMetrics),
    "admin":       (aggregate_admin_metrics, AdminMetrics),
}


def aggregate_all_metrics():
    """
    Aggregates and stores all metrics in a consistent way for the current day.
    Each aggregator returns a dict: metric_name -> (value, unit).
    """
    today = date.today()
    logger.info("Starting full metrics aggregation for %s", today)

    try:
        init_metrics_engine()
        logger.debug("Metrics database initialized.")

        primary_db = PrimarySessionLocal()
        metrics_db = MetricsSessionLocal()

        record_counts = {}

        try:
            for category, (aggregator, model_cls) in METRIC_SOURCES.items():
                logger.debug("Aggregating %s metrics...", category)
                metrics = aggregator(primary_db, today) if "date" in aggregator.__code__.co_varnames \
                    else aggregator(primary_db)

                if not isinstance(metrics, dict):
                    raise TypeError(f"{aggregator.__name__} must return a dict[str, (value, unit)]")

                for metric_name, (value, unit) in metrics.items():
                    metrics_db.add(model_cls(
                        date=today,
                        metric_name=metric_name,
                        value=value,
                        unit=unit
                    ))

                record_counts[category] = len(metrics)
                logger.debug("%s metrics aggregated: %d", category, record_counts[category])

            metrics_db.commit()
            logger.info("Metrics aggregation complete: %s", record_counts)

        except Exception:
            metrics_db.rollback()
            raise

        finally:
            primary_db.close()
            metrics_db.close()

    except Exception as e:
        logger.exception("Aggregation failed due to error: %s", e)
        raise
