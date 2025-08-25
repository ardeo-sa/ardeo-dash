"""
Defines the Program model representing medical programs in the healthcare system.

This module includes the Program SQLAlchemy model, which stores information about scheduled
programs, their associated consultants, institutions, and medical specialities. It is used to
organize and track structured clinical activities within healthcare institutions.
"""

from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base

class Program(Base):
    """
    Represents a medical program within the healthcare system, capturing details about its group,
    scheduling, and associated consultant. This model is essential for organizing
    and managing healthcare programs across different specialities and institutions.

    Attributes:
    program_id : int  Unique identifier for the program.
    program_group_code : str  Code representing the program group, used for categorization and reference.
    program_date : datetime  Date and time when the program is scheduled.
    consultant_code : str Code identifying the consultant associated with the program.
    consultant_forename : str  First name of the consultant involved in the program.
    consultant_surname : str   Last name of the consultant involved in the program.
    institution_code : str  Code representing the institution hosting the program.
    speciality : str  Medical speciality associated with the program, indicating the area of focus.
    """
    __tablename__ = 'program'

    program_id = Column(Integer, primary_key=True, nullable=False)
    program_group_code = Column(String, nullable=False)
    program_date = Column(DateTime)
    consultant_code = Column(String)
    consultant_forename = Column(String)
    consultant_surname = Column(String)
    institution_code = Column(String)
    speciality = Column(String, nullable=False)
