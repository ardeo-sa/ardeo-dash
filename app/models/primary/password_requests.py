"""
Manages password reset requests within the system, providing a secure mechanism for users
to reset their passwords through token-based validation.

Attributes:
----------
id : int
    Unique identifier for each password request.
created_date : datetime
    Timestamp indicating when the password reset request was created.
is_password_updated : str
    Flag indicating whether the password has been successfully updated ("Yes" or "No").
is_url_used : str
    Flag indicating whether the reset URL has been used ("Yes" or "No").
token : str
    Unique token for validating the password reset request.
user_id : int
    Identifier for the user who initiated the password reset request.
"""

from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base

class PasswordRequests(Base):
    """
    Manages password reset requests within the system, providing a secure mechanism for users
    to reset their passwords through token-based validation.

    Attributes:
    id : int  Unique identifier for each password request.
    created_date : datetime Timestamp indicating when the password reset request was created.
    is_password_updated : str  Flag indicating whether the password has been successfully updated ("Yes" or "No").
    is_url_used : str  Flag indicating whether the reset URL has been used ("Yes" or "No").
    token : str  Unique token for validating the password reset request.
    user_id : int Identifier for the user who initiated the password reset request.
    """
    __tablename__ = 'password_requests'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    is_password_updated = Column(String)
    is_url_used = Column(String)
    token = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
