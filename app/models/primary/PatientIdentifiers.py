from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PatientIdentifiers(Base):
    __tablename__ = 'patient_identifiers'

    patient_id = Column(Integer, ForeignKey('patient.patient_id'), primary_key=True, nullable=False)
    patient_hospitalNumber = Column(String)
    pas_context_id = Column(Integer, ForeignKey('pas_context.pas_context_id'), primary_key=True, nullable=False)
    patient = relationship('Patient')
    pas_context = relationship('Pas_context')
