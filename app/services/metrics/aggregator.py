"""
This module aggregates various types of metrics from the primary database and stores them in the metrics database.
The metrics include patient, MDT (Multidisciplinary Team), pathway, and operational metrics.
Each metric category is calculated using specific business logic and is persisted into separate tables
in the metrics database.

The following metrics are aggregated:
1. Patient Metrics: Includes metrics like average length of stay and admission count.
2. MDT Metrics: Includes metrics like MDT meeting count, average attendance, average wait time,
and MDT action completion rate.
3. Pathway Metrics: Includes metrics like readmission rate, no-show rate, and admission to treatment time.
4. Operational Metrics*: Includes general KPIs such as bed occupancy rate.

Functions:
- `aggregate_all_metrics`: The main entry point for aggregating and saving all metrics.
"""

from datetime import date
from app.database.primary import PrimarySessionLocal
from app.database.metrics import MetricsSessionLocal, init_metrics_db

from app.models.metrics import (
    PatientMetrics,
    MDTMetrics,
    PathwayMetrics,
    OperationalMetrics,
)

from app.services.metrics.operational import (
    get_admissions_discharge_counts,
    calculate_avg_length_of_stay,
    calculate_bed_occupancy,
)

from app.services.metrics.mdt import (
    calculate_mdt_meeting_count,
    calculate_mdt_avg_attendance,
    calculate_mdt_avg_wait_time,
    calculate_mdt_action_completion_rate,
)

from app.services.metrics.pathway import (
    calculate_pathway_adherence_rate,
    calculate_pathway_dropout_rate,
    calculate_pathway_success_rate,
    calculate_pathway_failure_rate,
    calculate_readmission_rate,
    calculate_admit_to_treatment_time,
    calculate_no_show_rate,
)


def aggregate_all_metrics():
    """
    Aggregates and stores all metrics, including patient metrics, MDT metrics, pathway metrics,
    and operational metrics for the current day.

    This function:
    - Fetches relevant data from the primary database.
    - Computes the necessary metrics using the data.
    - Saves the aggregated metrics in the metrics database.

    The metrics are saved in their respective tables: PatientMetrics, MDTMetrics, PathwayMetrics, and OperationalMetrics

    Args:
        None

    Returns:
        None
    """
    today = date.today()
    init_metrics_db()

    with PrimarySessionLocal() as primary_db, MetricsSessionLocal() as metrics_db:
        # ----- Patient Metrics -----
        admissions, discharges = get_admissions_discharge_counts(primary_db, today)
        avg_los = calculate_avg_length_of_stay(primary_db)

        patient_metrics = PatientMetrics(
            date=today,
            admission_count=admissions,
            avg_length_of_stay=avg_los
        )
        metrics_db.add(patient_metrics)

        # ----- MDT Metrics -----
        mdt_metrics = MDTMetrics(
            date=today,
            meeting_count=calculate_mdt_meeting_count(primary_db, today),
            avg_attendance=calculate_mdt_avg_attendance(primary_db, today),
            avg_wait_time=calculate_mdt_avg_wait_time(primary_db),
            action_completion_rate=calculate_mdt_action_completion_rate(primary_db)
        )
        metrics_db.add(mdt_metrics)

        # ----- Pathway Metrics -----
        pathway_metrics = PathwayMetrics(
            date=today,
            avg_admission_to_treatment_days=calculate_admit_to_treatment_time(primary_db),
            readmission_rate_30d=calculate_readmission_rate(primary_db),
            no_show_rate=calculate_no_show_rate(primary_db),
            adherence_rate=calculate_pathway_adherence_rate(primary_db),
            dropout_rate=calculate_pathway_dropout_rate(primary_db),
            success_rate=calculate_pathway_success_rate(primary_db),
            failure_rate=calculate_pathway_failure_rate(primary_db),
        )
        metrics_db.add(pathway_metrics)

        # ----- Operational Metrics (general KPIs) -----
        bed_occ = calculate_bed_occupancy(primary_db, today)
        metrics_db.add(OperationalMetrics(
            date=today,
            metric_name="bed_occupancy_rate",
            value=bed_occ,
            unit="percent"
        ))

        metrics_db.commit()
