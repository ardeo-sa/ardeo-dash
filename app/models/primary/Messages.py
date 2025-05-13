from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Messages(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, nullable=False)
    isacknowledged = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    message_content = Column(String)
    message_subject = Column(String)
    patient_id = Column(Integer, ForeignKey('patient.patient_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    patient = relationship('Patient')
    users = relationship('Users')
