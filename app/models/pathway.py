# app/models/pathway.py

from enum import Enum as PyEnum

from sqlalchemy import  Column, Integer, Enum, Boolean, DateTime

from app.database.metrics import Base


class PathwayStatusEnum(str, PyEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"


class PathwayOutcomeEnum(str, PyEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    UNKNOWN = "unknown"


class PathwayProgress(Base):
    __tablename__ = "pathway_progress"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    steps_total = Column(Integer)
    steps_completed = Column(Integer)
    status = Column(Enum(PathwayStatusEnum, name="pathway_status_enum"))
    outcome = Column(Enum(PathwayOutcomeEnum, name="pathway_outcome_enum"))
    readmitted = Column(Boolean, default=False)
    admission_time = Column(DateTime, nullable=True)
    treatment_start_time = Column(DateTime, nullable=True)
    diagnosis_time = Column(DateTime, nullable=True)
    treatment_end_time = Column(DateTime, nullable=True)
    had_complication = Column(Boolean, default=False)
    had_relapse = Column(Boolean, default=False)