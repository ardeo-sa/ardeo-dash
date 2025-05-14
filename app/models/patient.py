"""
This module defines the `Patient` SQLAlchemy model, representing a patient in the healthcare system.

The `Patient` model stores information about individual patients, including their personal details and
admission/discharge dates. It also establishes a relationship with the `ReferralAdmission` model, tracking
any referral admissions associated with the patient.

Attributes:
    id (int): Unique identifier for the patient.
    name (str): Name of the patient.
    admission_date (datetime): Date the patient was admitted to the healthcare system.
    discharge_date (datetime): Date the patient was discharged from the healthcare system.
    referral_admissions (relationship): One-to-many relationship to the `ReferralAdmission` model,
        tracking all referral admissions for this patient.
"""

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Patient(Base):
    """
        SQLAlchemy model representing a patient in the healthcare system.

        This model contains personal details about a patient, including their name, admission date, and discharge
        date. Additionally, it establishes a relationship with the `ReferralAdmission` model, allowing the system
        to track any referrals associated with the patient.

        Attributes:
            id (int): Primary key, unique identifier for the patient record.
            name (str): The name of the patient.
            admission_date (datetime): The date the patient was admitted.
            discharge_date (datetime): The date the patient was discharged.
            referral_admissions (relationship): One-to-many relationship with the `ReferralAdmission` model,
                which tracks all referral admissions associated with this patient.
    """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    admission_date = Column(Date)
    discharge_date = Column(Date)


    referral_admissions = relationship('ReferralAdmission', back_populates='patient')
