from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PatientCareProviders(Base):
    __tablename__ = 'patient_care_providers'

    careProvider_id = Column(Integer, ForeignKey('patient.patient_id'), primary_key=True, nullable=False)
    patient_hospitalNumber = Column(String)
    careProviderDetailsMap_KEY = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    patient = relationship('Patient')
    users = relationship('Users')
