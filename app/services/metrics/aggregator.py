"""
This module defines the `aggregate_operational_metrics` function that aggregates various operational metrics
from the primary database and stores them in the secondary metrics database.

The following metrics are aggregated:
1. Daily Admissions
2. Daily Discharges
3. Average Length of Stay
4. MDT Referral to Review Wait Time
5. Readmissions within 30 Days
6. No-show / Cancellation Rate for Appointments

These metrics are calculated based on data from tables such as `ReferralAdmission`, `MDTMeeting`, and `Appointment`.

The aggregated metrics are then stored in the `OperationalMetrics` table in the metrics database.
"""
from datetime import datetime
from sqlalchemy import func

from app.database.metrics import init_metrics_db, MetricsSessionLocal
from app.database.primary import PrimarySessionLocal
from app.models.admissions import ReferralAdmission
from app.models.appointments import Appointment
from app.models.mdt import MDTMeeting
from app.models.metrics import OperationalMetrics


def aggregate_operational_metrics():
    """
    Aggregates operational metrics from the primary database and stores them in the secondary metrics database.

    The function calculates the following metrics for the current date:
    1. **Daily Admissions**: Count of admissions for the day.
    2. **Daily Discharges**: Count of discharges for the day.
    3. **Average Length of Stay (LOS)**: Average number of days between admission and discharge.
    4. **MDT Referral to Review Wait Time**: Average number of days between referral time and review time in MDT meetings.
    5. **Readmissions within 30 Days**: Count of patients readmitted within 30 days of their previous discharge.
    6. **No-show / Cancellation Rate**: Percentage of missed or cancelled appointments out of the total appointments.

    The function performs the following steps:
    1. Fetches the relevant data from the primary database using SQLAlchemy queries.
    2. Aggregates the metrics based on the fetched data.
    3. Stores the aggregated metrics in the `OperationalMetrics` table in the metrics database.

    Returns:
        None
    """
    today = datetime.today().date()
    init_metrics_db()

    with PrimarySessionLocal() as session:
        # 1. Daily Admissions/Discharges
        daily_admissions = session.query(func.count()).filter(func.date(ReferralAdmission.admit_time) == today).scalar()
        daily_discharges = session.query(func.count()).filter(
            func.date(ReferralAdmission.discharge_time) == today).scalar()

        # 2. Average Length of Stay
        stays = session.query(ReferralAdmission).filter(ReferralAdmission.discharge_time.isnot(None)).all()
        los_list = [(a.discharge_time - a.admit_time).days for a in stays if a.admit_time and a.discharge_time]
        avg_los = sum(los_list) / len(los_list) if los_list else 0

        # 3. MDT Referral to Review Wait Time
        wait_times = session.query(MDTMeeting).filter(MDTMeeting.referral_time.isnot(None),
                                                      MDTMeeting.review_time.isnot(None)).all()
        mdt_waits = [(m.review_time - m.referral_time).days for m in wait_times]
        avg_mdt_wait = sum(mdt_waits) / len(mdt_waits) if mdt_waits else 0

        # 4. Readmissions within 30 days
        readmissions = 0
        admissions = session.query(ReferralAdmission).order_by(ReferralAdmission.patient_id,
                                                               ReferralAdmission.admit_time).all()
        last_admit = {}
        for a in admissions:
            if a.patient_id in last_admit:
                delta = (a.admit_time - last_admit[a.patient_id]).days
                if 0 < delta <= 30:
                    readmissions += 1
            last_admit[a.patient_id] = a.discharge_time

        # 5. No-show/Cancellation Rate
        appts = session.query(Appointment).all()
        total_appts = len(appts)
        missed = sum(1 for a in appts if not a.attended or a.cancelled)
        no_show_rate = (missed / total_appts) * 100 if total_appts else 0

    # Store metrics in secondary DB
    with MetricsSessionLocal() as session:
        def add_metric(name, value, unit):
            metric = OperationalMetrics(date=today, metric_name=name, value=value, unit=unit)
            session.add(metric)

        add_metric("daily_admissions", daily_admissions, "count")
        add_metric("daily_discharges", daily_discharges, "count")
        add_metric("average_length_of_stay", avg_los, "days")
        add_metric("average_mdt_wait_time", avg_mdt_wait, "days")
        add_metric("readmission_rate_30d", readmissions, "count")
        add_metric("appointment_no_show_rate", no_show_rate, "percent")

        session.commit()
