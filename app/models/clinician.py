
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Clinician(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_role = Column(String)
    referral_admissions = relationship('ReferralAdmission', back_populates='clinician')