"""
Module defining the AfFormData ORM model.

This module provides a SQLAlchemy model for storing detailed consultation form data,
including metadata, user associations, and XML-encoded form values.

It supports parsing of embedded form values via a property for convenient access.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base
from app.models.primary.parser.af_form_data_values_parser import parse_form_values

class AfFormData(Base):
    """
    Represents the form data entries within the application, capturing detailed records of consultation notes and
    associated metadata.

    Attributes:
    ----------
    af_type : str
        The type of the form.
    af_id : int
        Unique identifier for the form data entry.
    creation_date : datetime
        Timestamp when the form data was created.
    deleted : str
        Flag indicating if the form data is marked as deleted.
    editable : str
        Flag indicating if the form data is editable.
    afo_id : int
        Identifier for the associated form object.
    guid : str
        Globally unique identifier for the form entry.
    modified_date : datetime
        Timestamp when the form data was last modified.
    xml : str
        XML string storing the detailed consultation note data.
    episode_id : int
        Identifier for the associated episode.
    locked : str
        Flag indicating if the form data is locked.
    locked_by : str
        User who locked the form data.
    locked_date : datetime
        Timestamp when the form data was locked.
    referral_id : int
        Identifier for the associated referral.
    created_user : int
        Foreign key linking to the Users model for the creator.
    modified_user : int
        Foreign key linking to the Users model for the last modifier.

    Relationships:
    --------------
    createdUser : relationship
        Relationship with the Users model for the creator.
    modifiedUser : relationship  Users model for the last modifier.

    Properties:
    values : property Parses and returns form values from the XML string.
    """
    __tablename__ = 'af_form_data'

    af_type = Column(String, nullable=False)
    af_id = Column(Integer, primary_key=True, nullable=False)
    creation_date = Column(DateTime)
    deleted = Column(String)
    editable = Column(String)
    afo_id = Column(Integer)
    guid = Column(String, nullable=False)
    modified_date = Column(DateTime)
    xml = Column(String)
    episode_id = Column(Integer)
    locked = Column(String)
    locked_by = Column(String)
    locked_date = Column(DateTime)
    referral_id = Column(Integer)
    created_user = Column(Integer, ForeignKey('users.user_id'))
    modified_user = Column(Integer, ForeignKey('users.user_id'))
    createdUser = relationship('Users', foreign_keys=[created_user])
    modifiedUser = relationship('Users', foreign_keys=[modified_user])
    @property
    def values(self):
        """
            Parses and returns the form values from the XML data.

            Returns:
                The result of parsing the XML content, typically a structured
                representation (e.g., dict) of the form values extracted from the XML.
        """
        return parse_form_values(self.xml)
