"""
Represents a clinical episode within the healthcare system,
capturing essential details and associations for managing patient care.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base
from app.models.primary import Pathway


class Episode(Base):
    """
    Represents a clinical episode within the healthcare system,
     capturing essential details and associations for managing patient care.
    Attributes:
    episode_id : int  Unique identifier for the episode.
    guid : str Globally unique identifier for the episode.
    modified_date : datetime Timestamp of the last modification to the episode details.
    speciality : str Medical specialty associated with the episode.
    start_date : datetime  Date when the episode began.
    status : str Current status of the episode (e.g., active, suspended,discharged).
    subject_id : int  Foreign key linking to the subject (patient) associated with the episode.
    item_index : int  Index for ordering items within the episode context.
    assistant_id : int Foreign key linking to the assistant managing the episode.
    primary_specialist_id : int Foreign key linking to the primary specialist responsible for the episode.
    pathway_id : int  Foreign key linking to the associated care pathway.
    Relationships:
    assistant :   Relationship with the Users model for the assistant.
    primary_specialist :   Relationship with the Users model for the primary specialist.
    subject :   Relationship with the Subject model for the patient.
    pathway :  Relationship with the Pathway model for the care pathway."""
    __tablename__ = 'episode'

    episode_id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    speciality = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    status = Column(String)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)

    item_index = Column(Integer)

    assistant_id = Column(Integer, ForeignKey('users.user_id'))
    assistant = relationship('Users', foreign_keys=[assistant_id])

    primary_specialist_id = Column(Integer, ForeignKey('users.user_id'))
    primary_specialist = relationship('Users', foreign_keys=[primary_specialist_id])

    subject = relationship('Subject',foreign_keys=[subject_id])
    pathway_id = Column(Integer, ForeignKey('pathway.id'))
    pathway = relationship(Pathway)