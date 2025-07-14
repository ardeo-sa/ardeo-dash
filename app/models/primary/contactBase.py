from sqlalchemy import Column, Integer, String
from app.config import Base



class ContactBase(Base):
    """
    Serves as the foundational model for contact information,
    capturing essential details about an individual or organization.

    Attributes:
    contact_id : int Unique identifier for the contact.
    contact_dept : str Department associated with the contact.
    contact_asstName : str Name of the contact's assistant.
    contact_mngrName : str Name of the contact's manager.
    contact_spseName : str  Name of the contact's spouse.
    contact_office : str Office location of the contact.
    contact_org : str  Organization with which the contact is affiliated.
    contact_profession : str  Profession of the contact.
    """
    __tablename__ = 'contact_base'

    contact_id = Column(Integer, primary_key=True, nullable=False)
    contact_dept = Column(String)
    contact_asstName = Column(String)
    contact_mngrName = Column(String)
    contact_spseName = Column(String)
    contact_office = Column(String)
    contact_org = Column(String)
    contact_profession = Column(String)
