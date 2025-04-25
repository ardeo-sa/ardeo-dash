# app/models/pathway.py

from sqlalchemy import Column, Integer, String, Enum
from app.database.metrics import Base
from enum import Enum as PyEnum

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
