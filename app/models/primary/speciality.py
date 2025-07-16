"""
Medical speciality for categorizing healthcare disciplines.
"""

from sqlalchemy import Column, Integer, String
from app.config import Base

class Speciality(Base):
    """
     Represents a medical speciality within the healthcare system, providing a structured
     way to categorize and manage medical disciplines.
    This model is essential for organizing and tracking patient care across various
    areas of expertise.
    Attributes:
    id : int Unique identifier for the speciality.
    code : int  Numerical code representing the speciality, often used for system integration.
    description : str Descriptive name of the speciality.
    """
    __tablename__ = 'speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
