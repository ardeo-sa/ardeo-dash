from sqlalchemy import Column, Integer, Float, Date, String

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


class MDTMetrics(Base):
    __tablename__ = "mdt_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    meeting_count = Column(Integer, nullable=False)
    avg_attendance = Column(Float, nullable=False)
    avg_wait_time = Column(Float, nullable=False)  # in days
    action_completion_rate = Column(Float, nullable=False)  # percent


class PathwayMetrics(Base):
    __tablename__ = "pathway_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    avg_admission_to_treatment_days = Column(Float, nullable=False)
    readmission_rate_30d = Column(Float, nullable=False)
    no_show_rate = Column(Float, nullable=False)  # percent
