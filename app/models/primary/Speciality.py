from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Speciality(Base):
    __tablename__ = 'speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
