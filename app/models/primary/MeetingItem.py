from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MeetingItem(Base):
    __tablename__ = 'meeting_item'

    meetingitem_id = Column(Integer, primary_key=True, nullable=False)
    blogging_allowed = Column(String)
    meetingitem_cnId = Column(Integer)
    meetingitem_discussed = Column(String)
    meetingitem_formDefId = Column(Integer)
    guid = Column(String, nullable=False)
    meetingitem_action = Column(String)
    meetingitem_action_completed = Column(String)
    meetingitem_notes = Column(String)
    meetingitem_notdiscreason = Column(String)
    meetingitem_type = Column(String)
    patient_id = Column(Integer, ForeignKey('patient.patient_id'), nullable=False)
    meeting_id = Column(Integer, ForeignKey('meeting.meeting_id'))
    item_index = Column(Integer)
    patient = relationship('Patient')
    meeting = relationship('Meeting')
