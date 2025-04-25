
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import METRICS_DB_URI


metrics_engine = create_engine(METRICS_DB_URI, echo=True)
MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)

Base = declarative_base()

from app.models.metrics import PatientMetrics
from app.models.patient import Patient

Base.metadata.create_all(bind=metrics_engine)