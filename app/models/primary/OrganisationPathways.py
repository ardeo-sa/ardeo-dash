from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class OrganisationPathways(Base):
    __tablename__ = 'organisation_pathways'

    id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    is_published = Column(String)
    organisation_id = Column(Integer, ForeignKey('organisation.id'))
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'))
    organisation = relationship('Organisation')
    pathway = relationship('Pathway')
