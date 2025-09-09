"""
This module defines SQLAlchemy ORM models for tracking the progress of patient pathways within the healthcare system.

It includes the following models:

1. `PathwayStatusEnum`: Enum for tracking the status of a patient's pathway (e.g., active, completed, or dropped).
2. `PathwayOutcomeEnum`: Enum for tracking the outcome of a patient's pathway (e.g., success, failure, or unknown).
3. `PathwayProgress`: Tracks the progress of a patient's pathway, including key milestones, status, and outcomes.
It records information like:
    - Total steps and steps completed in the pathway.
    - Whether the patient was readmitted, had complications, or experienced a relapse.
    - Dates for various stages in the pathway such as admission, treatment start, diagnosis, and treatment end.

The `PathwayProgress` model helps in monitoring the patient’s journey through their treatment pathway,
providing insights into treatment success and possible issues like complications or readmissions.
"""
from enum import Enum as PyEnum

from sqlalchemy import  Column, Integer, Enum, Boolean, DateTime

from app.database.metrics import Base


class PathwayStatusEnum(str, PyEnum):
    """
    Enum for tracking the status of a patient's pathway.

    Attributes:
        ACTIVE (str): Indicates that the patient's pathway is active.
        COMPLETED (str): Indicates that the patient's pathway has been completed.
        DROPPED (str): Indicates that the patient's pathway has been dropped.
    """
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"


class PathwayOutcomeEnum(str, PyEnum):
    """
    Enum for tracking the outcome of a patient's pathway.

    Attributes:
        SUCCESS (str): Indicates that the patient's pathway was successful.
        FAILURE (str): Indicates that the patient's pathway failed.
        UNKNOWN (str): Indicates that the outcome of the patient's pathway is unknown.
    """
    SUCCESS = "success"
    FAILURE = "failure"
    UNKNOWN = "unknown"


class PathwayProgress(Base):
    """
    Tracks the progress of a patient's treatment pathway.

    This model records key milestones, status, and outcomes in the patient's pathway, including:
    - Total steps and steps completed in the pathway.
    - The current status (active, completed, dropped) and outcome (success, failure, unknown) of the pathway.
    - Information regarding whether the patient was readmitted, had complications, or experienced a relapse.
    - Dates for various stages in the pathway such as admission, treatment start, diagnosis, and treatment end.

    Attributes:
        id (int): Primary key for the pathway progress record.
        patient_id (int): The ID of the patient whose pathway is being tracked.
        steps_total (int): The total number of steps in the pathway.
        steps_completed (int): The number of steps completed in the pathway.
        status (PathwayStatusEnum): The current status of the pathway (e.g., active, completed, dropped).
        outcome (PathwayOutcomeEnum): The outcome of the pathway (e.g., success, failure, unknown).
        readmitted (bool): Indicates whether the patient was readmitted.
        admission_time (datetime): The date and time the patient was admitted to the pathway.
        treatment_start_time (datetime): The date and time the treatment started.
        diagnosis_time (datetime): The date and time the diagnosis was made.
        treatment_end_time (datetime): The date and time the treatment ended.
        had_complication (bool): Indicates whether the patient had any complications during the pathway.
        had_relapse (bool): Indicates whether the patient had a relapse during the pathway.
    """
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
