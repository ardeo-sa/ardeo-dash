# app/models/mdt.py

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class MDTMeeting(Base):
    __tablename__ = "mdt_meetings"

    id = Column(Integer, primary_key=True)
    meeting_time = Column(DateTime)
    referral_time = Column(DateTime)
    review_time = Column(DateTime)
    meeting_start_time = Column(DateTime)
    meeting_end_time = Column(DateTime)

    participants = relationship("MDTParticipant", back_populates="meeting")
    actions = relationship("MDTAction", back_populates="meeting")
    cases = relationship("MDTCase", back_populates="meeting")

class MDTParticipant(Base):
    __tablename__ = "mdt_participants"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    clinician_id = Column(Integer, ForeignKey("users.id"))

    meeting = relationship("MDTMeeting", back_populates="participants")


class MDTAction(Base):
    __tablename__ = "mdt_actions"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    completed = Column(Boolean, default=False)

    meeting = relationship("MDTMeeting", back_populates="actions")


class MDTCase(Base):
    __tablename__ = "mdt_cases"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("mdt_meetings.id"))
    patient_id = Column(Integer)  # optional: ForeignKey to patient table if it exists
    discussion_notes = Column(String, nullable=True)

    meeting = relationship("MDTMeeting", back_populates="cases")