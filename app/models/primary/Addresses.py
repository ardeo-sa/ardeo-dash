from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Addresses(Base):
    __tablename__ = 'addresses'

    contact_id = Column(Integer, ForeignKey('contact_base.contact_id'), primary_key=True, nullable=False)
    address_id = Column(Integer, ForeignKey('address.address_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    contact_base = relationship('Contact_base')
    address = relationship('Address')
