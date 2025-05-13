from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Meeting(Base):
    __tablename__ = 'meeting'

    meeting_id = Column(Integer, primary_key=True, nullable=False)
    meeting_date = Column(DateTime, nullable=False)
    email_summary_id = Column(Integer)
    meeting_end_date = Column(DateTime)
    formPath = Column(String)
    guid = Column(String, nullable=False)
    is_quorate = Column(String)
    meeting_location = Column(String)
    locked = Column(String)
    meetingRoom = Column(String)
    meeting_notes = Column(String)
    meeting_org_email_address = Column(String)
    summary_id = Column(Integer)
    meeting_title = Column(String, nullable=False)
    treatment_decision = Column(String)
    speciality = Column(String)
    is_virtual_meeting = Column(String)
    hospital_id = Column(Integer, ForeignKey('organisation.id'))
    organisation = relationship('Organisation')
