from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ClinicPatient(Base):
    __tablename__ = 'clinic_patient'

    clinic_id = Column(Integer, ForeignKey('clinic.clinic_id'), primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.patient_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    clinic = relationship('Clinic')
    patient = relationship('Patient')
