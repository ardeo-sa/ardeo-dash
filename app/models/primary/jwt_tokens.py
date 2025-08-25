"""
Manages JSON Web Tokens (JWTs) used for API authentication within the system,
tracking their status and association with users.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base

class JwtTokens(Base):
    """
    Manages JSON Web Tokens (JWTs) used for API authentication within the system,
     tracking their status and association with users.
    Attributes:
    id : int  Unique identifier for the JWT token record.
    expired : str Flag indicating whether the token is expired ("Yes" or "No").
    revoked : str   Flag indicating whether the token has been revoked ("Yes" or "No").
    token : str  The JWT string used for authentication.
    tokenType : str Type of the token (e.g., access, refresh).
    user_id : int  Foreign key linking to the user associated with the token.

    Relationships:
    users : Relationship with the Users model to access user details.
    """
    __tablename__ = 'jwt_tokens'

    id = Column(Integer, primary_key=True, nullable=False)
    expired = Column(String, nullable=False)
    revoked = Column(String, nullable=False)
    token = Column(String)
    tokenType = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
