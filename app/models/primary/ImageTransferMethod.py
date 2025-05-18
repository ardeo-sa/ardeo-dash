from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageTransferMethod(Base):
    __tablename__ = 'image_transfer_method'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String)
    image_transfer_interface = Column(String)
    image_transfer_code = Column(String, nullable=False)
    max_hours = Column(Integer)
