from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FormSequence(Base):
    __tablename__ = 'form_sequence'

    id = Column(Integer, primary_key=True, nullable=False)
    current_value = Column(Integer, nullable=False)
    format_mask = Column(String)
    increment = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    prefix = Column(String)
    suffix = Column(String)
