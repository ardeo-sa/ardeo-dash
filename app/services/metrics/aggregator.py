from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.database.primary import PrimarySessionLocal
from app.database.metrics import MetricsSessionLocal
from app.models.admissions import ReferralAdmission
from app.models.mdt import MDTMeeting
from app.models.appointments import Appointment
from app.models.metrics import OperationalMetrics

def aggregate_operational_metrics():
    today = datetime.today().date()

    with PrimarySessionLocal() as session:
        # 1. Daily Admissions/Discharges
        daily_admissions = session.query(func.count()).filter(func.date(ReferralAdmission.admit_time) == today).scalar()
        daily_discharges = session.query(func.count()).filter(func.date(ReferralAdmission.discharge_time) == today).scalar()

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
        admissions = session.query(ReferralAdmission).order_by(ReferralAdmission.patient_id, ReferralAdmission.admit_time).all()
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
