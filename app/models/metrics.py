
from sqlalchemy import Column, Integer, Float, Date
from app.database.metrics import Base


class PatientMetrics(Base):
    __tablename__ = "patient_metrics"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    avg_length_of_stay = Column(Float)
    admission_count = Column(Integer)


