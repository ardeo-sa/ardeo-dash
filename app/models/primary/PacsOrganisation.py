from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PacsOrganisation(Base):
    __tablename__ = 'pacs_organisation'

    pacs_id = Column(Integer, ForeignKey('pacs.id'), primary_key=True, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisation.id'), primary_key=True, nullable=False)
    pacs = relationship('Pacs')
    organisation = relationship('Organisation')
