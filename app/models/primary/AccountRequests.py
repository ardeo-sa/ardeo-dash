from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AccountRequests(Base):
    __tablename__ = 'account_requests'

    id = Column(Integer, primary_key=True, nullable=False)
    create_date = Column(DateTime)
    email = Column(String, nullable=False)
    is_url_used = Column(String)
    token = Column(String, nullable=False)
