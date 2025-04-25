# app/models/pathway.py

from sqlalchemy import Column, Integer, String, Enum
from app.database.base import Base

class PathwayStatusEnum(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"

class PathwayOutcomeEnum(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    UNKNOWN = "unknown"

class PathwayProgress(Base):
    __tablename__ = "pathway_progress"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    steps_total = Column(Integer)
    steps_completed = Column(Integer)
    status = Column(Enum(PathwayStatusEnum))
    outcome = Column(Enum(PathwayOutcomeEnum))
