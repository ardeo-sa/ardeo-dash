"""
This module defines the `ReferralAdmission` model and its associated enumeration used for tracking
referral-based admissions in the healthcare system.

The module includes:
- `ReferralStatusEnum`: Enumeration for referral/admission lifecycle statuses.
- `ReferralAdmission`: SQLAlchemy model representing a referral or admission record, linked to patients,
  clinicians, and treatment plans.
"""
import enum

from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.metrics import Base


# Enum for different admission statuses
class ReferralStatusEnum(enum.Enum):
    """
        Enum representing possible statuses for a referral or admission.

        Values:
            - PENDING: The referral is initiated but not yet acted upon.
            - REFERRED_IN: The patient has been referred into the system.
            - REFERRED_OUT: The patient has been referred to an external service.
            - DISCHARGED: The patient has been discharged from care.
            - COMPLETED: The treatment or referral process is complete.
            - CANCELLED: The referral was cancelled before action.
    """
    PENDING = "Pending"
    REFERRED_IN = "Referred In"
    REFERRED_OUT = "Referred Out"
    DISCHARGED = "Discharged"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ReferralAdmission(Base):
    """
        SQLAlchemy model for storing referral or admission information for a patient.

        Attributes:
            id (int): Primary key identifier.
            admit_time (datetime): Timestamp of the patient's admission.
            discharge_time (datetime): Timestamp of the patient's discharge.
            patient_id (int): Foreign key to the associated patient.
            referral_date (date): Date the referral was made.
            discharge_date (date): Date of discharge (if applicable).
            referral_status (ReferralStatusEnum): Status of the referral process.
            referral_type (str): Indicates the direction of referral, e.g., "In" or "Out".
            clinician_id (int): Foreign key to the clinician handling the referral.
            treatment_plan_id (int): Foreign key to an associated treatment plan (if any).
            discharge_notes (str): Optional notes recorded at discharge.

        Relationships:
            patient: Linked patient record.
            clinician: Linked clinician handling the case.
            treatment_plan: Linked treatment plan (if assigned).
    """
    __tablename__ = 'referral_admissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admit_time = Column(DateTime, nullable=True)
    discharge_time = Column(DateTime, nullable=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)  # Foreign key to Patient
    referral_date = Column(Date, nullable=True)  # Date of referral
    discharge_date = Column(Date, nullable=True)  # Date of discharge, if applicable
    referral_status = Column(Enum(ReferralStatusEnum), default=ReferralStatusEnum.PENDING)  # Status of the referral
    referral_type = Column(String, nullable=False)  # e.g., 'In' or 'Out'
    referring_clinician_id = Column(Integer, ForeignKey('clinician.id'), nullable=False)  # Foreign key to clinician handling the referral
    receiving_clinician_id = Column(Integer, ForeignKey('clinician.id'))
    receiving_organisation_id= Column(Integer, ForeignKey('organisation.id'))
    # treatment_plan_id = Column(Integer, ForeignKey('treatments.id'), nullable=True)  # If treatment is assigned
    pathway_id = Column(Integer, ForeignKey('pathway_progress.id'))
    discharge_notes = Column(String, nullable=True)  # Additional notes on discharge

    # Relationships
    receiving_clinician = relationship('Clinician', foreign_keys=[receiving_clinician_id],
                                       back_populates='referrals_received')
    referring_clinician = relationship('Clinician', foreign_keys=[referring_clinician_id],
                                       back_populates='referrals_made')
    patient = relationship('Patient', back_populates='referral_admissions')
    # treatment_plan = relationship('Treatment', back_populates='referral_admissions')
    pathwayProgress = relationship('PathwayProgress')
    organisation = relationship('Organisation', foreign_keys=[receiving_organisation_id])

    def __repr__(self):
        return (f"<ReferralAdmission(id={self.id}, patient_id={self.patient_id}, "
                f"referral_status={self.referral_status}, referral_type={self.referral_type})>")
