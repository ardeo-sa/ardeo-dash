from sqlalchemy import Column, Integer, String
from app.config import Base

class Address(Base):
    __tablename__ = 'address'

    class_type = Column(String, nullable=False)
    address_id = Column(Integer, primary_key=True, nullable=False)
    address_type = Column(String, nullable=False)
    address_value = Column(String, nullable=False)
