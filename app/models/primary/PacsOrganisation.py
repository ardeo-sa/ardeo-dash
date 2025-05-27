from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class PacsOrganisation(Base):
    __tablename__ = 'pacs_organisation'

    pacs_id = Column(Integer, ForeignKey('pacs.id'), primary_key=True, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisation.id'), primary_key=True, nullable=False)
    pacs = relationship('Pacs')
    organisation = relationship('Organisation')
