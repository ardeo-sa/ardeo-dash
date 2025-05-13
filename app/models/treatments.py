# app/models/treatments.py
"""
This module defines the `Treatment` SQLAlchemy model, representing a treatment plan in the healthcare system.

The `Treatment` model tracks treatment details for patients, which can be associated with referral admissions.

Attributes:
    id (int): Unique identifier for the treatment record.
    name (str): The name of the treatment plan (e.g., 'Chemotherapy', 'Surgery').
    referral_admissions (list of `ReferralAdmission`): One-to-many relationship to referral admissions associated
    with this treatment plan.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Treatment(Base):
    """
        SQLAlchemy model representing a treatment plan in the healthcare system.

        This model captures details about treatments provided to patients, including the name of the treatment
        and its association with referral admissions. A treatment plan can be linked to one or more referral
        admissions.

        Attributes:
            id (int): Primary key, unique identifier for the treatment plan.
            name (str): The name of the treatment (e.g., 'Chemotherapy', 'Surgery').
            referral_admissions (list of `ReferralAdmission`): One-to-many relationship with referral admissions
            associated with the treatment.
    """
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    referral_admissions = relationship('ReferralAdmission', back_populates='treatment_plan')
