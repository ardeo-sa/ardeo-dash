from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MeetingLocations(Base):
    __tablename__ = 'meeting_locations'

    meeting_Id = Column(Integer, ForeignKey('organisation.id'), primary_key=True, nullable=False)
    Location = Column(String)
    child_index = Column(Integer, primary_key=True, nullable=False)
    organisation = relationship('Organisation')
