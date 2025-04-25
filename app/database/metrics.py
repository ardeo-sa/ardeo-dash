
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import METRICS_DB_URI

metrics_engine = create_engine(METRICS_DB_URI)

MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)

Base = declarative_base()

from app.models.admissions import ReferralAdmission
from app.models.appointments import Appointment
from app.models.clinician import Clinician
from app.models.mdt import MDTMeeting
from app.models.pathway import PathwayProgress
from app.models.metrics import PatientMetrics, OperationalMetrics
from app.models.patient import Patient
from app.models.treatments import Treatments

Base.metadata.create_all(bind=metrics_engine)
