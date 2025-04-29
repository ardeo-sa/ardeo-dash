from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PacsHospital(Base):
    __tablename__ = 'pacs_hospital'

    pacs_id = Column(Integer, ForeignKey('pacs.id'), primary_key=True, nullable=False)
    hospital_id = Column(Integer, ForeignKey('organisation.id'), primary_key=True, nullable=False)
    pacs = relationship('Pacs')
    organisation = relationship('Organisation')
