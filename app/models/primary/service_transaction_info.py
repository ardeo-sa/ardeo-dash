"""
Tracks service transactions, associating them with users for auditing and monitoring.

Attributes:
- id: Unique identifier for the transaction.
- created_date: Timestamp of transaction initiation.
- session_key: Unique session key for tracking.
- user_id: Foreign key to the initiating user.

Relationships:
- users: Access to the related user details.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class ServiceTransactionInfo(Base):
    """
    Tracks information about service transactions, associating them with users and providing
    a mechanism for managing and auditing service usage.
    This model is crucial for monitoring and understanding service interactions within the system.

    Attributes:
    id : int  Unique identifier for the service transaction.
    created_date : datetime  Timestamp indicating when the service transaction was initiated.
    session_key : str Unique session key associated with the transaction, used for tracking and identification.
    user_id : int  Foreign key linking to the Users model, identifying the user who initiated the transaction.

    Relationships:
     users :  Relationship with the Users model to access user details.
    """
    __tablename__ = 'service_transaction_info'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    session_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    users = relationship('Users')
