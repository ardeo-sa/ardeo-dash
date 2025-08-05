"""
This module aggregates various types of metrics from the primary database and stores them in the metrics database.

Functions:
- `aggregate_all_metrics`: The main entry point for aggregating and saving all metrics.
"""
import logging
from datetime import date

from app.database.primary import PrimarySessionLocal
from app.database.metrics import MetricsSessionLocal, init_metrics_db

from app.models.metrics import (
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

def aggregate_all_metrics():
    """
    Aggregates and stores all metrics, including operational, MDT metrics, pathway metrics, referral, clinician
    and admin for the current day.

    This function:
    - Fetches relevant data from the primary database.
    - Computes the necessary metrics using the data.
    - Saves the aggregated metrics in the metrics database.

    The metrics are saved in their respective tables:
    MDTMetrics, PathwayMetrics, and OperationalMetrics

    Args:
        None

    Returns:
        None
    """
    today = date.today()
    logging.info("Starting full metrics aggregation for %s", today)

    try:
        init_metrics_db()
        logging.debug("Metrics database initialized.")

        with PrimarySessionLocal() as primary_db, MetricsSessionLocal() as metrics_db:
            record_counts = {}

            # ----- Operational Metrics -----
            operational = aggregate_operational_metrics(primary_db)
            for name, (value, unit) in operational.items():
                metrics_db.add(OperationalMetrics(
                    date=today,
                    metric_name=name,
                    value=value,
                    unit=unit
                ))
            record_counts['operational'] = len(operational)
            logging.debug("Operational metrics aggregated: %d", record_counts['operational'])

            # ----- MDT Metrics -----
            mdt = aggregate_mdt_metrics(primary_db)
            for name, (value, unit) in mdt.items():
                metrics_db.add(MDTMetrics(
                    date=today,
                    metric_name=name,
                    meeting_count=value,
                    avg_attendance=value,
                    avg_wait_time=unit,
                    action_completion_rate=True
                ))
            record_counts['mdt'] = len(mdt)
            logging.debug("MDT metrics aggregated: %d", record_counts['mdt'])

            # ----- Pathway Metrics -----
            pathway = aggregate_pathway_metrics(primary_db)
            for name, (value, unit) in pathway.items():
                metrics_db.add(PathwayMetrics(
                    date=today,
                    metric_name=name,
                    avg_admission_to_treatment_days=value,
                    readmission_rate_30d=value,
                    no_show_rate=unit
                ))
            record_counts['pathway'] = len(pathway)
            logging.debug("Pathway metrics aggregated: %d", record_counts['pathway'])


            # ----- Referral Metrics -----
            referral = aggregate_referral_metrics(primary_db, today)
            for name, (value, unit) in referral.items():
                metrics_db.add(ReferralMetrics(
                    date=today,
                    metric_name=name,
                    value=value,
                    unit=unit
                ))
            record_counts['referral'] = len(referral)
            logging.debug("Referral metrics aggregated: %d", record_counts['referral'])

            # ----- Clinician Metrics -----
            clinician = aggregate_clinician_metrics(primary_db)
            for name, (value, unit) in clinician.items():
                metrics_db.add(ClinicianMetrics(
                    date=today,
                    metric_name=name,
                    value=value,
                    unit=unit
                ))
            record_counts['clinician'] = len(clinician)
            logging.debug("Clinician metrics aggregated: %d", record_counts['clinician'])

            # ----- Admin Metrics -----
            admin = aggregate_admin_metrics(primary_db)
            for name, (value, unit) in admin.items():
                metrics_db.add(AdminMetrics(
                    date=today,
                    metric_name=name,
                    value=value,
                    unit=unit
                ))
            record_counts['admin'] = len(admin)
            logging.debug("Admin metrics aggregated: %d", record_counts['admin'])

            metrics_db.commit()
            logging.info("Metrics aggregation complete and committed: %s", record_counts)

    except Exception as e:
        logging.exception("Aggregation failed due to error: %s", e)
        raise

