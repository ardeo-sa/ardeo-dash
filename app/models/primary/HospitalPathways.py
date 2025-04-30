from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class HospitalPathways(Base):
    __tablename__ = 'hospital_pathways'

    hospital_pathway_id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    is_published = Column(String)
    hospital_id = Column(Integer, ForeignKey('organisation.id'))
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'))
    organisation = relationship('Organisation')
    pathway = relationship('Pathway')
