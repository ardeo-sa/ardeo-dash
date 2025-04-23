from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MDTMeeting(Base):
    __tablename__ = "mdt_meetings"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    referral_time = Column(DateTime)
    review_time = Column(DateTime)
    participants = Column(String)
