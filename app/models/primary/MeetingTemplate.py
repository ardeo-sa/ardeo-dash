from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MeetingTemplate(Base):
    __tablename__ = 'meeting_template'

    id = Column(Integer, primary_key=True, nullable=False)
    day_of_week = Column(String)
    end_time = Column(String)
    formPath = Column(String)
    meeting_location = Column(String)
    speciality = Column(String)
    speciality_description = Column(String)
    start_time = Column(String)
    treatment_decision = Column(String)
    is_virtual_meeting = Column(String)
    hospital_id = Column(Integer, ForeignKey('organisation.id'))
    ps_id = Column(Integer, ForeignKey('summary.id'))
    organisation = relationship('Organisation')
    summary = relationship('Summary')
