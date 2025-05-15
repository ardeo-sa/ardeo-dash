from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PasswordRequests(Base):
    __tablename__ = 'password_requests'

    id = Column(Integer, primary_key=True, nullable=False)
    createdDate = Column(DateTime)
    isPasswordUpdated = Column(String)
    isUrlUsed = Column(String)
    token = Column(String, nullable=False)
    USER_ID = Column(Integer, nullable=False)
