# app/models/referral.py

from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    source = Column(String)  # e.g., "Primary Care", "ED", "Internal Transfer"
