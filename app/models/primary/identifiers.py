"""
Represents the association between subjects (patients) and their unique identifiers across different contexts.
This model facilitates the management of patient identifiers within a healthcare system,
ensuring each identifier is unique within its context.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base

class Identifiers(Base):
    """
    Represents the association between subjects (patients) and their unique identifiers across different contexts.
    This model facilitates the management of patient identifiers within a healthcare system,
    ensuring each identifier is unique within its context.
    Attributes:
    subject_id : int Foreign key linking to the Subject model, representing the patient.
    identifier : strUnique identifier for the subject within the specified context.
    context_id : int Foreign key linking to the IdentifierContext model, defining the namespace for the identifier.

    Relationships:
    subject : Relationship with the Subject model to access patient details.
    identifier_context : Relationship with the IdentifierContext model to access context details.

    """
    __tablename__ = 'identifiers'

    subject_id = Column(Integer, ForeignKey('subject.subject_id'), primary_key=True, nullable=False)
    identifier = Column(String)
    context_id = Column(Integer, ForeignKey('identifier_context.context_id'), primary_key=True, nullable=False)
    subject = relationship('Subject')
    identifier_context = relationship('IdentifierContext')
