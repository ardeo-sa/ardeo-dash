# app/models/treatments.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.metrics import Base

class Treatments(Base):
    __tablename__ = "treatments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    referral_admissions = relationship('ReferralAdmission', back_populates='treatment_plan')