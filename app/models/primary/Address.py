from sqlalchemy import Column, Integer, String
from app.config import Base

class Address(Base):
    """
    Represents a physical or virtual address in the system, encompassing various types and values.
    Attributes:
    class_type : str  The classification type of the address.
    address_id : int Unique identifier for the address.
    address_type : str  Defines the type of address
    address_value : str The actual address details.
    """
    __tablename__ = 'address'

    class_type = Column(String, nullable=False)
    address_id = Column(Integer, primary_key=True, nullable=False)
    address_type = Column(String, nullable=False)
    address_value = Column(String, nullable=False)
