from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base

class OtpInfo(Base):
    """
    Manages one-time password (OTP) information for two-factor authentication (2FA) during
    login processes, providing an additional security layer by verifying user identities.

    Attributes:
    id : int Unique identifier for the OTP record.
    created_date : datetime Date and time when the OTP was generated.
    email : str Email address associated with the OTP, used for user identification.
    is_used : str  Flag indicating whether the OTP has been used ("Yes" or "No").
    otp : str The one-time password used for 2FA.
    """
    __tablename__ = 'otp_info'

    id = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime)
    email = Column(String, nullable=False)
    is_used = Column(String)
    otp = Column(String, nullable=False)
