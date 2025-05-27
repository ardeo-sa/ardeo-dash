from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



class ServiceTransactionInfo(Base):
    __tablename__ = 'service_transaction_info'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    session_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    users = relationship('Users')
