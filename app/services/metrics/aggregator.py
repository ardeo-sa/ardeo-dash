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
    calculate_avg_mdt_wait_time,
    calculate_readmissions,
    calculate_no_show_rate,
    calculate_admit_to_treatment_time,
)

from app.services.metrics.mdt import (
    calculate_mdt_meeting_count,
    calculate_mdt_avg_attendance,
    calculate_mdt_avg_wait_time,
    calculate_mdt_action_completion_rate,
    calculate_mdt_avg_case_discussion_time,
)

from app.services.metrics.pathway import (
    calculate_pathway_adherence_rate,
    calculate_pathway_dropout_rate,
    calculate_pathway_success_rate,
    calculate_pathway_failure_rate,
    calculate_readmission_rate,
    calculate_admit_to_treatment_time,
    calculate_diagnosis_to_treatment_time,
    calculate_treatment_duration,
    calculate_complication_rate,
    calculate_relapse_rate,
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
            action_completion_rate=calculate_mdt_action_completion_rate(primary_db),
            discussion_time=calculate_mdt_avg_case_discussion_time(primary_db)
        )
        metrics_db.add(mdt_metrics)

        # ----- Pathway Metrics -----
        pathway_metrics = PathwayMetrics(
            date=today,
            avg_admission_to_treatment_days=calculate_admit_to_treatment_time(primary_db),
            readmission_rate_30d=calculate_readmission_rate(primary_db),
            adherence_rate=calculate_pathway_adherence_rate(primary_db),
            dropout_rate=calculate_pathway_dropout_rate(primary_db),
            success_rate=calculate_pathway_success_rate(primary_db),
            failure_rate=calculate_pathway_failure_rate(primary_db),
            diagnosis_to_treatment_days=calculate_diagnosis_to_treatment_time(primary_db),
            avg_treatment_duration_days=calculate_treatment_duration(primary_db),
            complication_rate=calculate_complication_rate(primary_db),
            relapse_rate=calculate_relapse_rate(primary_db),
        )
        metrics_db.add(pathway_metrics)

        # ----- Operational Metrics (general KPIs) -----
        operational_metrics = OperationalMetrics(
            date=today,
            daily_admissions=admissions,
            daily_discharges=discharges,
            average_length_of_stay=calculate_avg_length_of_stay(primary_db),
            average_mdt_wait_time=calculate_avg_mdt_wait_time(primary_db),
            readmission_rate_30d=calculate_readmissions(primary_db),
            appointment_no_show_rate=calculate_no_show_rate(primary_db),
            bed_occupancy_rate=calculate_bed_occupancy(primary_db, today),
            admission_to_treatment_start=calculate_admit_to_treatment_time(primary_db),
        )
        metrics_db.add(operational_metrics)

        metrics_db.commit()
