"""
This module defines the models for Multidisciplinary Team (MDT) meetings, participants, actions, and cases.

The following entities are defined:
- MDTMeeting: Represents an MDT meeting, including meeting times and relationships with participants, actions, and cases
- MDTParticipant: Represents participants (clinicians) in an MDT meeting.
- MDTAction: Represents actions taken during an MDT meeting.
- MDTCase: Represents cases discussed in an MDT meeting, typically linked to a patient.

Each class contains relationships to other entities involved in the MDT process.
"""
# app/models/mdt.py

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class MDTMeeting(Base):
    """
        SQLAlchemy model representing an MDT (Multidisciplinary Team) meeting.

        Attributes:
            id (int): Primary key of the meeting.
            meeting_time (datetime): The time the meeting was scheduled.
            referral_time (datetime): The time the referral for the meeting was made.
            review_time (datetime): The time the case review took place.
            meeting_start_time (datetime): The actual start time of the meeting.
            meeting_end_time (datetime): The actual end time of the meeting.

        Relationships:
            participants (MDTParticipant): List of participants in the meeting.
            actions (MDTAction): List of actions discussed during the meeting.
            cases (MDTCase): List of cases (patients) discussed in the meeting.
        """
    __tablename__ = "mdt_meetings"

    id = Column(Integer, primary_key=True)
    primary_guid= Column(String, nullable=False)
    meeting_time = Column(DateTime)
    referral_time = Column(DateTime)
    review_time = Column(DateTime)
    meeting_start_time = Column(DateTime)
    meeting_end_time = Column(DateTime)

    participants = relationship("MDTParticipant", back_populates="meeting")
    actions = relationship("MDTAction", back_populates="meeting")
    cases = relationship("MDTCase", back_populates="meeting")

class MDTParticipant(Base):
    """
        SQLAlchemy model representing a participant (clinician) in an MDT meeting.

        Attributes:
            id (int): Primary key of the participant record.
            meeting_id (int): Foreign key referencing the MDT meeting this participant attended.
            clinician_id (int): Foreign key referencing the clinician (user) participating in the meeting.

        Relationships:
            meeting (MDTMeeting): The MDT meeting this participant is associated with.
    """
    __tablename__ = "mdt_participants"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    clinician_id = Column(Integer, ForeignKey("users.id"))

    meeting = relationship("MDTMeeting", back_populates="participants")


class MDTAction(Base):
    """
        SQLAlchemy model representing an action assigned or discussed during an MDT meeting.

        Attributes:
            id (int): Primary key of the action.
            meeting_id (int): Foreign key referencing the MDT meeting this action is linked to.
            completed (bool): A flag indicating whether the action has been completed.

        Relationships:
            meeting (MDTMeeting): The MDT meeting this action is associated with.
    """
    __tablename__ = "mdt_actions"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    completed = Column(Boolean, default=False)

    meeting = relationship("MDTMeeting", back_populates="actions")


class MDTCase(Base):
    """
        SQLAlchemy model representing a case (patient) discussed during an MDT meeting.

        Attributes:
            id (int): Primary key of the case record.
            meeting_id (int): Foreign key referencing the MDT meeting the case was discussed in.
            patient_id (int): Foreign key referencing the patient associated with this case.
            discussion_notes (str): Notes from the meeting about the case.

        Relationships:
            meeting (MDTMeeting): The MDT meeting where this case was discussed.
    """
    __tablename__ = "mdt_cases"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    patient_id = Column(Integer)  # optional: ForeignKey to patient table if it exists
    discussion_notes = Column(String, nullable=True)

    meeting = relationship("MDTMeeting", back_populates="cases")
