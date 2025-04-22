
from sqlalchemy.orm import Session
from datetime import date
from app.database.primary import PrimarySessionLocal
from app.database.metrics import MetricsSessionLocal
from app.models.patient import Patient
from app.models.metrics import PatientMetrics
import datetime

def calculate_metrics():
    with PrimarySessionLocal() as session:
        patients = session.query(Patient).all()

    total_days = 0
    count = 0
    for patient in patients:
        if patient.admission_date and patient.discharge_date:
            stay = (patient.discharge_date - patient.admission_date).days
            total_days += stay
            count += 1

    avg_stay = total_days / count if count > 0 else 0

    with MetricsSessionLocal() as session:
        metric = PatientMetrics(
            date=datetime.date.today(),
            avg_length_of_stay=avg_stay,
            admission_count=len(patients)
        )
        session.add(metric)
        session.commit()
