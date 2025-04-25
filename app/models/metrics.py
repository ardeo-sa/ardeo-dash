
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from app.database.metrics import Base


class PatientMetrics(Base):
    __tablename__ = "patient_metrics"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    avg_length_of_stay = Column(Float)
    admission_count = Column(Integer)

class OperationalMetrics(Base):
    __tablename__ = "operational_metrics"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    metric_name = Column(String)
    value = Column(Float)
    unit = Column(String)


