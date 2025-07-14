"""
Defines the methods available for transferring images within the healthcare system,
including their interfaces and operational constraints.
"""

from sqlalchemy import Column, Integer, String
from app.config import Base

class ImageTransferMethod(Base):
    """
    Defines the methods available for transferring images within the healthcare system,
    including their interfaces and operational constraints.

    Attributes:
    id : int Unique identifier for the transfer method.
    description : str Textual description of the transfer method, providing context and details.
    image_transfer_interface : str  Interface used for the image transfer, detailing the technical means of execution.
    image_transfer_code : str Code representing the transfer method, required for identification and integration.
    max_hours : int   Maximum allowable hours for completing the transfer, serving as a time constraint.
    """
    __tablename__ = 'image_transfer_method'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String)
    image_transfer_interface = Column(String)
    image_transfer_code = Column(String, nullable=False)
    max_hours = Column(Integer)
