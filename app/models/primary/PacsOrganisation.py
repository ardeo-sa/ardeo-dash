from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class PacsOrganisation(Base):
    """
    Represents the association between PACS and organisations, facilitating the integration of imaging systems within healthcare networks.
    This model ensures that PACS configurations are properly linked to their respective organisations.
    Attributes:
    pacs_id : int Foreign key linking to the PACS model, identifying the PACS system involved.
    organisation_id : int  Foreign key linking to the Organisation model, identifying the organisation using the PACS.
    Relationships:
    pacs :   Relationship with the Pacs model to access PACS details.
    organisation : Relationship with the Organisation model to access organisational details.
    """
    __tablename__ = 'pacs_organisation'

    pacs_id = Column(Integer, ForeignKey('pacs.id'), primary_key=True, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisation.id'), primary_key=True, nullable=False)
    pacs = relationship('Pacs')
    organisation = relationship('Organisation')
