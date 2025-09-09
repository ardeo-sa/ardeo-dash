"""
    This module defines the `Referral` SQLAlchemy model, representing a referral record in the healthcare system.

    The `Referral` model tracks the source of the referral and the patient associated with it.

    Attributes:
        id (int): Unique identifier for the referral.
        patient_id (int): Foreign key referencing the associated patient.
        source (str): The source from which the referral was made (e.g., doctor, department).
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Referral(Base):
    """
        SQLAlchemy model representing a referral record in the healthcare system.

        This model contains details about the referral, including the patient it is associated with and the
        source of the referral. This helps track where the referral originated from, such as a doctor or a specific
        department.

        Attributes:
            id (int): Primary key, unique identifier for the referral record.
            patient_id (int): Foreign key linking the referral to the associated patient.
            source (str): The source from which the referral was made (e.g., doctor, department).
    """
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("clinician.id"), nullable=True)
    source = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    referral_date = Column(Date, nullable=True)

    patient = relationship("Patient")
    clinician = relationship("Clinician")
