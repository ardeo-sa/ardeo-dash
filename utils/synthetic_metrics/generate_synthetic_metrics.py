"""
Generate synthetic operational metrics data for a hospital.
Accepts parameters from the command line.
Simulates realistic daily metrics with fluctuations.
Saves them to a SQLite database matching the OperationalMetrics schema.
"""
import argparse
import random
import pandas as pd
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base

from clinician_registry import generate_clinician_registry, generate_clinician_daily_metrics


Base = declarative_base()


class GeneratedMetrics(Base):
    """
    Represents generated hospital metrics (operational or pathway).
    """
    __tablename__ = "generated_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    metric_name = Column(String)
    value = Column(Float)
    unit = Column(String)
    metric_type = Column(String)

def generate_metrics_for_day(date_, total_beds, daily_clinician_data):
    """
    Generate realistic synthetic metrics for a given date.

    Args:
        date_ (datetime.date): The date for the metrics.
        total_beds (int): Total number of hospital beds.

    Returns:
        List[GeneratedMetrics]: All metrics for the day.
    """

    # --- Operational metrics ---
    admissions = random.randint(30, 70)
    discharges = max(20, admissions - random.randint(0, 10))
    avg_los = round(random.uniform(3.5, 7.0), 2)
    mdt_wait = round(random.uniform(1.0, 4.5), 2)
    readmission_rate = round(random.uniform(5.0, 12.0), 2)
    no_show_rate = round(random.uniform(3.0, 10.0), 2)
    occupancy_rate = round(random.uniform(75.0, 95.0), 2)
    admit_to_treatment = round(random.uniform(0.5, 2.5), 2)

    operational_metrics = [
        ("daily_admissions", admissions, "count"),
        ("daily_discharges", discharges, "count"),
        ("average_length_of_stay", avg_los, "days"),
        ("average_mdt_wait_time", mdt_wait, "hours"),
        ("readmission_rate_30d", readmission_rate, "percent"),
        ("appointment_no_show_rate", no_show_rate, "percent"),
        ("bed_occupancy_rate", occupancy_rate, "percent"),
        ("admission_to_treatment_start", admit_to_treatment, "days"),
    ]

    # --- Pathway metrics ---
    adherence_rate = round(random.uniform(70.0, 90.0), 2)
    dropout_rate = round(random.uniform(5.0, 15.0), 2)
    success_rate = round(random.uniform(75.0, 95.0), 2)
    failure_rate = 100.0 - success_rate
    readmission_rate_pw = round(random.uniform(5.0, 12.0), 2)
    admit_to_treatment_pw = round(random.uniform(0.5, 2.5), 2)
    diagnosis_to_treatment = round(random.uniform(1.0, 4.0), 2)
    treatment_duration = round(random.uniform(5.0, 14.0), 2)
    complication_rate = round(random.uniform(3.0, 10.0), 2)
    relapse_rate = round(random.uniform(2.0, 8.0), 2)

    pathway_metrics = [
        ("pathway_adherence_rate", adherence_rate, "percent"),
        ("pathway_dropout_rate", dropout_rate, "percent"),
        ("pathway_success_rate", success_rate, "percent"),
        ("pathway_failure_rate", failure_rate, "percent"),
        ("pathway_readmission_rate", readmission_rate_pw, "percent"),
        ("pathway_admit_to_treatment_time", admit_to_treatment_pw, "days"),
        ("pathway_diagnosis_to_treatment_time", diagnosis_to_treatment, "days"),
        ("pathway_treatment_duration", treatment_duration, "days"),
        ("pathway_complication_rate", complication_rate, "percent"),
        ("pathway_relapse_rate", relapse_rate, "percent"),
    ]

    # --- Admin metrics ---
    patient_to_clinician = round(random.uniform(8.0, 15.0), 2)
    imaging_util = random.randint(20, 50)
    lab_util = random.randint(50, 100)
    treatment_slot_util = random.randint(10, 30)

    admin_metrics = [
        ("patient_to_clinician_ratio", patient_to_clinician, "ratio"),
        ("imaging_utilization", imaging_util, "count"),
        ("lab_test_utilization", lab_util, "count"),
        ("treatment_slot_utilization", treatment_slot_util, "count"),
    ]

    # --- MDT metrics ---
    mdt_meetings = random.randint(2, 5)
    mdt_attendance = round(random.uniform(6.0, 10.0), 2)
    mdt_wait_time = round(random.uniform(0.5, 2.0), 2)
    mdt_completion = round(random.uniform(80.0, 98.0), 2)
    mdt_case_time = round(random.uniform(5.0, 15.0), 2)

    mdt_metrics = [
        ("mdt_meeting_count", mdt_meetings, "count"),
        ("mdt_avg_attendance", mdt_attendance, "people"),
        ("mdt_avg_wait_time", mdt_wait_time, "days"),
        ("mdt_action_completion_rate", mdt_completion, "percent"),
        ("mdt_avg_case_discussion_time", mdt_case_time, "minutes"),
    ]

    # --- Referral metrics ---
    referral_volume = random.randint(40, 80)
    referral_conversion = round(random.uniform(60.0, 85.0), 2)
    referral_time = round(random.uniform(1.0, 3.0), 2)
    referral_sources = random.randint(5, 10)

    referral_metrics = [
        ("referral_volume_daily", referral_volume, "count"),
        ("referral_conversion_rate", referral_conversion, "percent"),
        ("referral_to_admission_time", referral_time, "days"),
        ("referral_source_count", referral_sources, "count"),
    ]


    # --- Clinician performance from individual data ---
    clinician_count = len([c for c in daily_clinician_data if not c["is_absent"]])
    clinician_absent_count = len([c for c in daily_clinician_data if c["is_absent"]])
    total_seen = sum(d["patients_seen"] for d in daily_clinician_data)
    total_admitted = sum(d["patients_admitted"] for d in daily_clinician_data)
    total_tasks = sum(d["tasks_completed"] for d in daily_clinician_data)
    total_clinicians = clinician_absent_count + clinician_count

    avg_seen = round(total_seen / clinician_count, 2) if clinician_count else 0
    avg_admitted = round(total_admitted / clinician_count, 2) if clinician_count else 0
    avg_tasks = round(total_tasks / clinician_count, 2) if clinician_count else 0
    absence_rate = round(clinician_absent_count / total_clinicians, 2) if total_clinicians else 0

    clinician_metrics = [
        ("active_clinicians", clinician_count, "count"),
        ("absent_clinicians", clinician_absent_count, "count"),
        ("absence_rate", absence_rate, "rate"),
        ("avg_patients_seen", avg_seen, "count"),
        ("avg_patients_admitted", avg_admitted, "count"),
        ("avg_tasks_completed", avg_tasks, "count"),
    ]


    # Compile all results into GeneratedMetrics objects
    results = []
    for name, value, unit in operational_metrics:
        results.append(
            GeneratedMetrics(date=date_, metric_name=name, value=value, unit=unit, metric_type="operational"))
    for name, value, unit in pathway_metrics:
        results.append(
            GeneratedMetrics(date=date_, metric_name=name, value=value, unit=unit, metric_type="pathway"))
    for name, value, unit in admin_metrics:
        results.append(
            GeneratedMetrics(date=date_, metric_name=name, value=value, unit=unit, metric_type="admin"))
    for name, value, unit in clinician_metrics:
        results.append(
            GeneratedMetrics(date=date_, metric_name=name, value=value, unit=unit, metric_type="clinician"))
    for name, value, unit in mdt_metrics:
        results.append(
            GeneratedMetrics(date=date_, metric_name=name, value=value, unit=unit, metric_type="mdt"))
    for name, value, unit in referral_metrics:
        results.append(
            GeneratedMetrics(date=date_, metric_name=name, value=value, unit=unit, metric_type="referral"))

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic operational hospital metrics data.")
    parser.add_argument("--days", type=int, default=30, help="Number of days of data to generate")
    parser.add_argument("--beds", type=int, default=100, help="Total number of hospital beds")
    parser.add_argument("--db", type=str, default="sqlite:///synthetic_metrics.db", help="Database URL")
    parser.add_argument("--csv", type=str, default="synthetic_metrics.csv", help="Output CSV file name.")
    args = parser.parse_args()

    engine = create_engine(args.db, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    clinician_roster = generate_clinician_registry(
        departments=["Oncology", "Cardiology", "Emergency", "General Medicine", "Surgery"],
        clinicians_per_dept=20
    )

    today = datetime.today().date()
    all_metrics = []
    clinician_daily_records = []

    for i in range(args.days):
        date_ = today - timedelta(days=i)
        daily_clinician_data = generate_clinician_daily_metrics(clinician_roster, date_)
        daily_metrics = generate_metrics_for_day(date_, args.beds, daily_clinician_data)

        session.add_all(daily_metrics)
        all_metrics.extend(daily_metrics)
        clinician_daily_records.extend(daily_clinician_data)

    session.commit()
    print(f"Inserted {len(all_metrics)} metrics across {args.days} days into {args.db}")

    # Save to CSV
    df = pd.DataFrame([{
        "date": m.date,
        "metric_name": m.metric_name,
        "value": m.value,
        "unit": m.unit,
        "metric_type": m.metric_type
    } for m in all_metrics])
    df.to_csv(args.csv, index=False)
    print(f"Exported to tall CSV: {args.csv}")

    # --- Save wide-format tables by metric_type ---
    for metric_type in df["metric_type"].unique():
        df_subset = df[df["metric_type"] == metric_type].copy()
        df_wide = df_subset.pivot(index="date", columns="metric_name", values="value")
        df_wide.reset_index(inplace=True)
        output_filename = f"{metric_type}_metrics_wide.csv"
        df_wide.to_csv(output_filename, index=False)
        print(f"Exported wide-format CSV: {output_filename}")

    # --- Save clinician data ---
    clinician_df = pd.DataFrame(clinician_daily_records)
    clinician_df.to_csv("clinician_daily_metrics.csv", index=False)
    print("Exported individual clinician daily performance to: clinician_daily_metrics.csv")

if __name__ == "__main__":
    main()
