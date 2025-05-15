"""
This module defines the `Clinician` model for storing basic user information
for healthcare professionals in the metrics database.

Clinicians are linked to referral admissions they are responsible for handling.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.metrics import Base

class Clinician(Base):
    """
        SQLAlchemy model representing a clinician (user) in the healthcare system.

        Attributes:
            id (int): Primary key for the clinician record.
            name (str): Name of the clinician.
            user_role (str): Role of the user (e.g., doctor, nurse, admin).
            referral_admissions (List[ReferralAdmission]): List of referral admissions handled by the clinician.
    """
    __tablename__ = "clinician"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_role = Column(String)

    # Relationships
    referral_admissions = relationship('ReferralAdmission', back_populates='clinician')
