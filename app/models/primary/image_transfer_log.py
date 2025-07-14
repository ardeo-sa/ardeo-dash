"""
Logs the details of image transfers within the healthcare system, capturing key events, errors,
and transfer methods for auditing and troubleshooting purposes.
"""

from sqlalchemy import Column, Integer, String, DateTime

from app.config import Base

class ImageTransferLog(Base):
    """
    Logs the details of image transfers within the healthcare system, capturing key events, errors,
     and transfer methods for auditing and troubleshooting purposes.
    Attributes:
    id : int  Unique identifier for the log entry.
    error_desc : str  Description of any errors encountered during the transfer.
    event_date : datetime  Date and time when the transfer event occurred.
    event_desc : str Description of the transfer event.
    accession_number : str  Accession number for the transferred image.
    note_id : int   Identifier for notes associated with the transfer.
    subject_id : int Identifier for the subject (patient) related to the image.
    transfer_method : str  Method used for transferring the image (e.g., DICOM, FTP).
    user_id : int Identifier for the user responsible for the transfer.

    """
    __tablename__ = 'image_transfer_log'

    id = Column(Integer, primary_key=True, nullable=False)
    error_desc = Column(String)
    event_date = Column(DateTime, nullable=False)
    event_desc = Column(String, nullable=False)
    accession_number = Column(String, nullable=False)
    note_id = Column(Integer, nullable=False)
    subject_id = Column(Integer, nullable=False)
    transfer_method = Column(String, nullable=False)
    user_id = Column(Integer)
