"""
This module aggregates various types of metrics from the primary database and stores them in the metrics database.

Functions:
- `aggregate_all_metrics`: The main entry point for aggregating and saving all metrics.
"""

from datetime import date

from app.database.primary import PrimarySessionLocal
from app.database.metrics import MetricsSessionLocal

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
    init_metrics_db()

    with PrimarySessionLocal() as primary_db, MetricsSessionLocal() as metrics_db:
        # ----- Operational Metrics -----
        for name, (value, unit) in aggregate_operational_metrics(primary_db).items():
            metrics_db.add(OperationalMetrics(
                date=today,
                metric_name=name,
                value=value,
                unit=unit
            ))

        # ----- MDT Metrics -----
        for name, (value, unit) in aggregate_mdt_metrics(primary_db).items():
            metrics_db.add(MDTMetrics(
                date=today,
                metric_name=name,
                meeting_count=value,
                avg_attendance=value,
                avg_wait_time=unit,
                action_completion_rate=True
            ))

        # ----- Pathway Metrics -----
        for name, (value, unit) in aggregate_pathway_metrics(primary_db).items():
            metrics_db.add(PathwayMetrics(
                date=today,
                metric_name=name,
                avg_admission_to_treatment_days=value,
                readmission_rate_30d=value,
                no_show_rate=unit
            ))
        # ----- Referral Metrics -----
        referral_metrics_dict = aggregate_referral_metrics(primary_db, today)
        for name, (value, unit) in referral_metrics_dict.items():
            metrics_db.add(
                ReferralMetrics(
                    date=today,
                    metric_name=name,
                    value=value,
                    unit=unit
                )
            )

        # ----- Clinician Metrics -----
        clinician_metrics_dict = aggregate_clinician_metrics(primary_db)
        for name, (value, unit) in clinician_metrics_dict.items():
            metrics_db.add(ClinicianMetrics(
                date=today,
                metric_name=name,
                value=value,
                unit=unit
            ))

        # ----- Admin Metrics -----
        admin_metrics_dict = aggregate_admin_metrics(primary_db)
        for name, (value, unit) in admin_metrics_dict.items():
            metrics_db.add(AdminMetrics(
                date=today,
                metric_name=name,
                value=value,
                unit=unit
            ))

        metrics_db.commit()
