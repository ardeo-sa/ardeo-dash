from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'

    class_type = Column(String, nullable=False)
    address_id = Column(Integer, primary_key=True, nullable=False)
    address_type = Column(String, nullable=False)
    address_value = Column(String, nullable=False)
