from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    admission_date = Column(Date)
    discharge_date = Column(Date)
    referral_admissions = relationship('ReferralAdmission', back_populates='patient')
