from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base



class PasswordRequests(Base):
    __tablename__ = 'password_requests'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    is_password_updated = Column(String)
    is_url_used = Column(String)
    token = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
