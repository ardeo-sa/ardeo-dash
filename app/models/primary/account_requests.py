"""
Module defining the AccountRequests ORM model.

This module contains the SQLAlchemy model for tracking user login account requests.
It includes fields for request metadata such as creation date, user email, verification token,
and whether the associated URL has been used.

The AccountRequests table supports managing and validating new account creation requests.
"""

from sqlalchemy import Column, Integer, String, DateTime

from app.config import Base


class AccountRequests(Base):
    """
       ORM model for tracking user login account requests.

       This table stores requests for new user accounts, including metadata
       such as request date, email, and a token used for secure verification.

       Attributes:
           id (int): Primary key for the account request.
           create_date (datetime): Timestamp when the account request was created.
           email (str): Email address of the user requesting access.
           is_url_used (str): Indicates whether the account creation URL has been used ('Y' or 'N').
           token (str): Secure token used to validate or verify the request.
       """
    __tablename__ = 'account_requests'

    id = Column(Integer, primary_key=True, nullable=False)
    create_date = Column(DateTime)
    email = Column(String, nullable=False)
    is_url_used = Column(String)
    token = Column(String, nullable=False)
