from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base



class ImageTransferLog(Base):
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
