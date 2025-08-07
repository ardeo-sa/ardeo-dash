"""
This module defines SQLAlchemy ORM models representing MDT (Multidisciplinary Team)
meeting-related data in the primary clinical database.

These models are used during data migration to extract MDT meetings, participants,
patient cases, and notes for import into the metrics database.

Tables modeled:
- mdt_meetings
- mdt_notes
- mdt_patient_cases
- mdt_participants
"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class PrimaryMDTMeeting(Base):
    """
    Represents a single MDT (Multidisciplinary Team) meeting in the primary database.

    Attributes:
        id (int): Unique identifier for the meeting.
        start_time (datetime): Meeting start time.
        end_time (datetime): Meeting end time.
        notes (list): List of PrimaryMDTNote associated with this meeting.
        patients (list): List of PrimaryMDTPatientCase discussed in this meeting.
        participants (list): List of PrimaryMDTParticipant who attended this meeting.
    """
    __tablename__ = "mdt_meetings"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    notes = relationship("PrimaryMDTNote", back_populates="meeting")
    patients = relationship("PrimaryMDTPatientCase", back_populates="meeting")
    participants = relationship("PrimaryMDTParticipant", back_populates="meeting")


class PrimaryMDTNote(Base):
    """
    Represents a note taken during an MDT meeting.

    Attributes:
        id (int): Unique identifier for the note.
        content (str): Text content of the note.
        meeting_id (int): Foreign key linking to the MDT meeting.
    """
    __tablename__ = "mdt_notes"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    meeting = relationship("PrimaryMDTMeeting", back_populates="notes")


class PrimaryMDTPatientCase(Base):
    """
    Represents a patient case discussed in an MDT meeting.

    Attributes:
        id (int): Unique identifier for the patient case.
        patient_id (int): Reference to the patient being discussed.
        meeting_id (int): Foreign key linking to the MDT meeting.
    """
    __tablename__ = "mdt_patient_cases"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, nullable=False)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    meeting = relationship("PrimaryMDTMeeting", back_populates="patients")


class PrimaryMDTParticipant(Base):
    """
    Represents a clinician participant in an MDT meeting.

    Attributes:
        id (int): Unique identifier for the participant record.
        clinician_id (int): ID of the clinician attending.
        meeting_id (int): Foreign key linking to the MDT meeting.
    """
    __tablename__ = "mdt_participants"

    id = Column(Integer, primary_key=True)
    clinician_id = Column(Integer, nullable=False)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    meeting = relationship("PrimaryMDTMeeting", back_populates="participants")
