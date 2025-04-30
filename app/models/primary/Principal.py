from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Principal(Base):
    __tablename__ = 'principal'

    principal_type = Column(String, nullable=False)
    principal_id = Column(Integer, primary_key=True, nullable=False)
    principal_name = Column(String, nullable=False)
    principal_unique = Column(String, nullable=False)
