from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base



class OtpInfo(Base):
    __tablename__ = 'otp_info'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    email = Column(String, nullable=False)
    is_used = Column(String)
    otp = Column(String, nullable=False)
