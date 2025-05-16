from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PatientCareProviders(Base):
    __tablename__ = 'patient_care_providers'

    careProvider_id = Column(Integer, ForeignKey('subject.subject_id'), primary_key=True, nullable=False)
    identifier = Column(String)
    careProviderDetailsMap_KEY = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    subject = relationship('Subject')
    users = relationship('Users')
