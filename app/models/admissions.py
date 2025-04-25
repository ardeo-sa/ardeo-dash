from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.metrics import Base
import enum

# Enum for different admission statuses
class ReferralStatusEnum(enum.Enum):
    PENDING = "Pending"
    REFERRED_IN = "Referred In"
    REFERRED_OUT = "Referred Out"
    DISCHARGED = "Discharged"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class ReferralAdmission(Base):
    __tablename__ = 'referral_admissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)  # Foreign key to Patient
    referral_date = Column(Date, nullable=True)  # Date of referral
    discharge_date = Column(Date, nullable=True)  # Date of discharge, if applicable
    referral_status = Column(Enum(ReferralStatusEnum), default=ReferralStatusEnum.PENDING)  # Status of the referral
    referral_type = Column(String, nullable=False)  # e.g., 'In' or 'Out'
    clinician_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to clinician handling the referral
    treatment_plan_id = Column(Integer, ForeignKey('treatments.id'), nullable=True)  # If treatment is assigned
    discharge_notes = Column(String, nullable=True)  # Additional notes on discharge

    # Relationships
    patient = relationship('Patient', back_populates='referral_admissions')
    clinician = relationship('Clinician', back_populates='referral_admissions')
    treatment_plan = relationship('Treatments', back_populates='referral_admissions')

    def __repr__(self):
        return f"<ReferralAdmission(id={self.id}, patient_id={self.patient_id}, referral_status={self.referral_status}, referral_type={self.referral_type})>"

