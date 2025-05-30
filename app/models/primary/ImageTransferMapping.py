from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class ImageTransferMapping(Base):
    __tablename__ = 'image_transfer_mapping'

    id = Column(Integer, primary_key=True, nullable=False)
    organisation_id = Column(Integer, nullable=False)
    is_preferred = Column(String)
    image_transfer_method_id = Column(Integer, ForeignKey('image_transfer_method.id'))
    image_transfer_method = relationship('Image_transfer_method')
