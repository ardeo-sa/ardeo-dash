from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AttendeeApproval(Base):
    __tablename__ = 'attendee_approval'

    attendeeapproval_id = Column(Integer, primary_key=True, nullable=False)
    attendeeapproval_agreed = Column(String)
    attendeeName = Column(String)
    attendeeapproval_comment = Column(String)
    meetingitem_id = Column(Integer, ForeignKey('meeting_item.meetingitem_id'))
    attendeeapproval_index = Column(Integer)
    meeting_item = relationship('Meeting_item')
