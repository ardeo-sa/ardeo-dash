from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MeetingScheduleUsers(Base):
    __tablename__ = 'meeting_schedule_users'

    meeting_schedule_id = Column(Integer, ForeignKey('meeting_template.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    meeting_template = relationship('Meeting_template')
    users = relationship('Users')
