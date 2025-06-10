from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base

class IepImageRequest(Base):
    """
       Represents a request for imaging exchange within the healthcare system,
       capturing details about the image request,
       transaction status, and institutional involvement.
    Attributes:
    iep_img_id : int  Unique identifier for the image request.
    accession_no : str Accession number associated with the image request.
    description : str Description of the image request.
    direction : str  Direction of the image request (e.g., inbound, outbound).
    initiating_institution : str  Institution that initiated the image request.
    last_updated : datetime   Timestamp of the last update to the image request.
    priority_name : str Priority level assigned to the image request.
    responding_institution : str  Institution responding to the image request.
    result_code : int  Code indicating the result of the image request.
    result_message : str  Message describing the result of the image request.
    send_to_worklist : str Indicator whether the request should be sent to a worklist.
    status_name : str  Current status of the image request.
    tracking_number : str  Tracking number for the image request.
    transaction_date : datetime Date of the transaction related to the image request.
    transaction_id : str Identifier for the transaction.
    type_name : str Type of image request.
    vendor_tx_code : str Vendor transaction code associated with the request.
    """
    __tablename__ = 'iep_image_request'

    iep_img_id = Column(Integer, primary_key=True, nullable=False)
    accession_no = Column(String, nullable=False)
    description = Column(String)
    direction = Column(String)
    initiating_institution = Column(String)
    last_updated = Column(DateTime)
    priority_name = Column(String)
    responding_institution = Column(String)
    result_code = Column(Integer)
    result_message = Column(String)
    send_to_worklist = Column(String)
    status_name = Column(String)
    tracking_number = Column(String)
    transaction_date = Column(DateTime)
    transaction_id = Column(String)
    type_name = Column(String)
    vendor_tx_code = Column(String)
