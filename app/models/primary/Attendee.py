from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Attendee(Base):
    __tablename__ = 'attendee'

    attendee_id = Column(Integer, primary_key=True, nullable=False)
    attendee_address = Column(String)
    attended_meeting = Column(String)
    is_chairperson = Column(String, nullable=False)
    is_coordinator = Column(String, nullable=False)
    attendee_fax = Column(String)
    attendee_method = Column(String)
    attendee_letter = Column(String)
    is_presence_mandatory = Column(String, nullable=False)
    attendee_telephone = Column(String)
    attendee_user_id = Column(Integer, ForeignKey('users.user_id'))
    meeting_id = Column(Integer, ForeignKey('meeting.meeting_id'))
    users = relationship('Users')
    meeting = relationship('Meeting')
