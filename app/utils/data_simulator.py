"""
Generate synthetic operational metrics data for a hospital.
Accepts parameters from the command line.
Simulates realistic daily metrics with fluctuations.
Saves them to a SQLite database matching the OperationalMetrics schema.
"""
import argparse
import random
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class OperationalMetrics(Base):
    """
    Represents operational metrics for a healthcare facility.
    """
    __tablename__ = "operational_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    metric_name = Column(String)
    value = Column(Float)
    unit = Column(String)


def generate_metrics_for_day(date_, total_beds):
    """
    Generate realistic operational metrics for a single day.

    Args:
        date_ (datetime.date): The date of the metric.
        total_beds (int): Total number of hospital beds.

    Returns:
        list of OperationalMetrics: Synthetic metrics for that date.
    """
    admissions = random.randint(30, 70)
    discharges = max(20, admissions - random.randint(0, 10))
    avg_los = round(random.uniform(3.5, 7.0), 2)
    mdt_wait = round(random.uniform(1.0, 4.5), 2)
    readmission_rate = round(random.uniform(5.0, 12.0), 2)
    no_show_rate = round(random.uniform(3.0, 10.0), 2)
    occupancy_rate = round(min(100.0, (random.uniform(0.75, 0.95) * total_beds / total_beds) * 100), 2)
    admit_to_treatment = round(random.uniform(0.5, 2.5), 2)

    return [
        OperationalMetrics(date=date_, metric_name="daily_admissions", value=admissions, unit="count"),
        OperationalMetrics(date=date_, metric_name="daily_discharges", value=discharges, unit="count"),
        OperationalMetrics(date=date_, metric_name="average_length_of_stay", value=avg_los, unit="days"),
        OperationalMetrics(date=date_, metric_name="average_mdt_wait_time", value=mdt_wait, unit="hours"),
        OperationalMetrics(date=date_, metric_name="readmission_rate_30d", value=readmission_rate, unit="percent"),
        OperationalMetrics(date=date_, metric_name="appointment_no_show_rate", value=no_show_rate, unit="percent"),
        OperationalMetrics(date=date_, metric_name="bed_occupancy_rate", value=occupancy_rate, unit="percent"),
        OperationalMetrics(date=date_, metric_name="admission_to_treatment_start", value=admit_to_treatment, unit="days"),
    ]


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic operational hospital metrics data.")
    parser.add_argument("--days", type=int, default=30, help="Number of days of data to generate")
    parser.add_argument("--beds", type=int, default=100, help="Total number of hospital beds")
    parser.add_argument("--db", type=str, default="sqlite:///synthetic_metrics.db", help="Database URL")
    args = parser.parse_args()

    engine = create_engine(args.db, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    today = datetime.today().date()
    for i in range(args.days):
        date_ = today - timedelta(days=i)
        metrics = generate_metrics_for_day(date_, args.beds)
        session.add_all(metrics)

    session.commit()
    print(f"✅ Generated {args.days} days of metrics in {args.db}")


if __name__ == "__main__":
    main()
