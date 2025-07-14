from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class Addresses(Base):
    """
    Manages the association between contacts and their addresses,
    allowing for efficient tracking and retrieval of address details linked to specific contacts.
    Attributes:
    contact_id : int
        Foreign key linking to ContactBase's contact_id.
    address_id : int
        Foreign key linking to Address's address_id.
    child_index : int
        Index to differentiate multiple addresses associated with the same contact.

    Relationships:
    contact_base : relationship Establishes a relationship with the ContactBase model.
    address : relationship Establishes a relationship with the Address model.
    """
    __tablename__ = 'addresses'

    contact_id = Column(Integer, ForeignKey('contact_base.contact_id'), primary_key=True, nullable=False)
    address_id = Column(Integer, ForeignKey('address.address_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    contact_base = relationship('Contact_base')
    address = relationship('Address')
