from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ServiceTransactionInfo(Base):
    __tablename__ = 'service_transaction_info'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    session_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    users = relationship('Users')
