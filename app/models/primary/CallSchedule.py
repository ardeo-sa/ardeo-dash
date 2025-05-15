from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CallSchedule(Base):
    __tablename__ = 'call_schedule'

    id = Column(Integer, primary_key=True, nullable=False)
    ardeoVideoUrl = Column(String)
    call_end_date = Column(DateTime, nullable=False)
    call_password = Column(String)
    call_start_date = Column(DateTime, nullable=False)
    callStatus = Column(Integer, nullable=False)
    creationDate = Column(DateTime)
    description = Column(String)
    call_externalReceivingUserEmails = Column(String)
    guid = Column(String)
    patientIncluded = Column(String)
    meetingId = Column(Integer)
    modifiedDate = Column(DateTime)
    title = Column(String)
    callingUserId = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    patientId = Column(Integer, ForeignKey('patient.patient_id'))
    users = relationship('Users')
    patient = relationship('Patient')
