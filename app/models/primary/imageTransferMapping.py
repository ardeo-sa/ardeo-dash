from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class ImageTransferMapping(Base):
    """
     Represents the mapping between organizations and their preferred image transfer methods,
     facilitating streamlined image exchanges in the healthcare system.
    Attributes:
    id : int  Unique identifier for the mapping entry.
    organisation_id : int   Identifier for the organization associated with the transfer method.
    is_preferred : str Flag indicating if the transfer method is the preferred choice for the organization.
    image_transfer_method_id : int Foreign key linking to the ImageTransferMethod model.

    Relationships:
    image_transfer_method : Relationship with the ImageTransferMethod model to access the details of the transfer method.
    """
    __tablename__ = 'image_transfer_mapping'

    id = Column(Integer, primary_key=True, nullable=False)
    organisation_id = Column(Integer, nullable=False)
    is_preferred = Column(String)
    image_transfer_method_id = Column(Integer, ForeignKey('image_transfer_method.id'))
    image_transfer_method = relationship('Image_transfer_method')
