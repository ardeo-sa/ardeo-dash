"""
Module for defining the Organisation model using SQLAlchemy ORM.

This module contains the Organisation class, which maps to the 'organisation'
table in the database and defines its schema using SQLAlchemy's declarative base.
"""
from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship

from app.database.metrics import Base

class Organisation(Base):
    """
        SQLAlchemy ORM model for the 'organisation' table.

        Attributes:
            id (int): Primary key, auto-incremented.
            name (str): Name of the organisation.
            code (str): Unique code for the organisation (non-nullable).
    """

    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, nullable=False)
