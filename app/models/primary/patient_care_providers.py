"""
Defines the model for linking patients to their care providers.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base

class PatientCareProviders(Base):
    """
    Represents the association between patients and their care providers,
    facilitating the management and coordination of patient care through specific provider assignments.
    This model is crucial for ensuring that each patient is linked to the appropriate care provider,
    supporting efficient and personalized healthcare delivery.

    Attributes:
    careProvider_id : int Foreign key linking to the Subject model, identifying the patient.
    identifier : str Identifier for the care provider, used for tracking and reference.
    careProviderDetailsMap_KEY : int  Foreign key linking to the Users model, identifying the care
    provider assigned to the patient.

    Relationships:
    subject :  Relationship with the Subject model to access patient details.
    users :  Relationship with the Users model to access care provider information.
    """
    __tablename__ = 'patient_care_providers'

    careProvider_id = Column(Integer, ForeignKey('subject.subject_id'), primary_key=True, nullable=False)
    identifier = Column(String)
    careProviderDetailsMap_KEY = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    subject = relationship('Subject')
    users = relationship('Users')
