from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Principal(Base):
    __tablename__ = 'principal'

    principal_type = Column(String, nullable=False)
    principal_id = Column(Integer, primary_key=True, nullable=False)
    principal_name = Column(String, nullable=False)
    principal_unique = Column(String, nullable=False)
