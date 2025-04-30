from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CallRecording(Base):
    __tablename__ = 'call_recording'

    id = Column(Integer, primary_key=True, nullable=False)
    ardeoVideoUrl = Column(String)
    callEndDate = Column(DateTime)
    callStartDate = Column(DateTime)
    recordingPath = Column(String)
