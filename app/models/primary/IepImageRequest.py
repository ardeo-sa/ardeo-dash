from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class IepImageRequest(Base):
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
