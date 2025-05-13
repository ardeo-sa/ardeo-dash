from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PatientNotes(Base):
    __tablename__ = 'patient_notes'

    id = Column(Integer, primary_key=True, nullable=False)
    note_type = Column(Integer, nullable=False)
    notes = Column(String)
    patient_id = Column(Integer, nullable=False)
