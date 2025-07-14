"""
Tracks the status of imaging requests and processes within the healthcare system,
providing key details on the imaging workflow and associated entities.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class ImagingStatus(Base):
    """
    Tracks the status of imaging requests and processes within the healthcare system,
    providing key details on the imaging workflow and associated entities.
    Attributes:
    imaging_status_id : int Unique identifier for the imaging status entry.
    accession_number : str  Accession number linked to the imaging record.
    episode_id : intIdentifier for the episode associated with the imaging.
    current_status : int Current status code indicating the progress or state of the imaging process.
    last_modified_date : datetimeTimestamp of the last modification to the imaging status.
    note_id : int Identifier for notes related to the imaging status.
    is_notified : str  Flag indicating if relevant parties have been notified of the status.
    start_date : datetime Date when the imaging process started.
    user_id : intIdentifier for the user managing or responsible for the imaging status.
    organisation_id : int Foreign key linking to the organisation involved in the imaging process.
    image_transfer_method_id : intForeign key linking to the method used for image transfer.
    subject_id : intForeign key linking to the subject (patient) associated with the imaging.

    Relationships:
    organisation : Relationship with the Organisation model to access organisational details.
    image_transfer_method : Relationship with the ImageTransferMethod model to access transfer method details.
    subject : Relationship with the Subject model to access patient details.
    """
    __tablename__ = 'imaging_status'

    imaging_status_id = Column(Integer, primary_key=True, nullable=False)
    accession_number = Column(String, nullable=False)
    episode_id = Column(Integer, nullable=False)
    current_status = Column(Integer, nullable=False)
    last_modified_date = Column(DateTime, nullable=False)
    note_id = Column(Integer, nullable=False)
    is_notified = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisation.id'))
    image_transfer_method_id = Column(Integer, ForeignKey('image_transfer_method.id'))
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    organisation = relationship('Organisation')
    image_transfer_method = relationship('Image_transfer_method')
    subject = relationship('Subject')
