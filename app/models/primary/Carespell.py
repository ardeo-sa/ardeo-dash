from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Carespell(Base):
    __tablename__ = 'carespell'

    carespell_id = Column(Integer, primary_key=True, nullable=False)
    carespell_extId = Column(String)
    isExternalcs = Column(String)
    guid = Column(String, nullable=False)
    carespell_modified_date = Column(DateTime, nullable=False)
    carespell_site = Column(String, nullable=False)
    carespell_start = Column(DateTime, nullable=False)
    status = Column(String)
    keyWorker_id = Column(Integer, ForeignKey('users.user_id'))
    patient_id = Column(Integer, ForeignKey('patient.patient_id'), nullable=False)
    primaryClinician_id = Column(Integer, ForeignKey('users.user_id'))
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'))
    item_index = Column(Integer)
    users = relationship('Users')
    patient = relationship('Patient')
    pathway = relationship('Pathway')
