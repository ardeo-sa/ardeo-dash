from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AttendeeRole(Base):
    __tablename__ = 'attendee_role'

    meeting_schedule_id = Column(Integer, ForeignKey('meeting_template.id'), primary_key=True, nullable=False)
    is_chairperson = Column(String, nullable=False)
    is_coordinator = Column(String, nullable=False)
    is_presenceMandatory = Column(String, nullable=False)
    attendeeRole_KEY = Column(Integer, primary_key=True, nullable=False)
    meeting_template = relationship('Meeting_template')
