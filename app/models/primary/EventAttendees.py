from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class EventAttendees(Base):
    __tablename__ = 'event_attendees'

    event_id = Column(Integer, ForeignKey('occurence.occurence_id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    occurence = relationship('Occurence')
    users = relationship('Users')
