"""
Represents a healthcare provider within the system,
capturing essential details about their contact information,
professional background, and organizational affiliations.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base

class CareProvider(Base):
    """
     Represents a healthcare provider within the system,
     capturing essential details about their contact information,
     professional background, and organizational affiliations.
    Attributes:
    id : int  Unique identifier for the care provider.
    address1 : str  Primary address line for the care provider.
    address2 : str   Secondary address line.
    address3 : str Tertiary address line.
    allowContactDisplay : str Flag indicating if contact information can be displayed publicly.
    city : str  City of the care provider's address.
    country : str  Country of the care provider's address.
    county : str County or region of the care provider's address.
    department : str  Department within the organization.
    job_title : str  Job title of the care provider.
    mobile_phone : str Mobile phone number.
    organisation_name : str  Name of the affiliated organization.
    personal_information_bio : str  Bio or personal information about the care provider.
    personal_url : str URL to the care provider's personal or professional page.
    postcode : str Postal code of the care provider's address.
    preferred_contact : str  Preferred method of contact.
    qualification : str Professional qualifications.
    secretary_name : str Name of the care provider's secretary.
    work_phone : str Work phone number.
    user_id : int  Identifier linking to the user associated with the care provider.
    Relationships:
    users : Relationship with the Users model to link user-specific information.
     """
    __tablename__ = 'care_provider'

    id = Column(Integer, primary_key=True, nullable=False)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    allowContactDisplay = Column(String)
    city = Column(String)
    country = Column(String)
    county = Column(String)
    department = Column(String)
    job_title = Column(String)
    mobile_phone = Column(String)
    organisation_name = Column(String)
    personal_information_bio = Column(String)
    personal_url = Column(String)
    postcode = Column(String)
    preferred_contact = Column(String)
    qualification = Column(String)
    secretary_name = Column(String)
    work_phone = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
