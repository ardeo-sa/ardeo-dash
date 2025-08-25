"""
Defines the model for storing provider details associated with a subject (patient).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class ProviderDetails(Base):
    """
     Captures comprehensive details about healthcare providers associated with patients,
      providing a structured approach to managing provider information throughout a
       patient's journey.  This model allows for tracking provider changes over time
       and facilitates efficient coordination of care.
    Attributes:
    id : intUnique identifier for the provider details record.
    action_date : datetimeDate and time when this provider detail record was added or updated.
    address : strProvider's address.
    country : str  Provider's country.
    email_address : str Provider's email address.
    full_name : str  Provider's full name.
    organisation_code : str Code identifying the provider's organization.
    organisation_name : str Name of the provider's organization.
    mobile_phone : str Provider's mobile phone number.
    subject_identifier : strIdentifier for the subject (patient) this record pertains to.
    postcode : strProvider's postal code.
    role : strProvider's role in the patient's care.
    speciality : strProvider's medical speciality.
    username : str  Provider's username in the system.
    work_phone : str Provider's work phone number.
    subject_id : int Foreign key linking to the Subject model, representing the patient.
    child_index : intIndex to manage multiple provider records for a single patient and track changes over time.

    Relationships:
    subject : Relationship with the Subject model to access patient information.
    """
    __tablename__ = 'provider_details'

    id = Column(Integer, primary_key=True, nullable=False)
    action_date = Column(DateTime)
    address = Column(String)
    country = Column(String)
    email_address = Column(String)
    full_name = Column(String)
    organisation_code = Column(String)
    organisation_name = Column(String)
    mobile_phone = Column(String)
    subject_identifier = Column(String)
    postcode = Column(String)
    role = Column(String)
    speciality = Column(String)
    username = Column(String)
    work_phone = Column(String)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    child_index = Column(Integer)
    subject = relationship('Subject')
