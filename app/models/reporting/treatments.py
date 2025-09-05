"""
This module defines the `Treatment` SQLAlchemy model, representing a treatment plan in the healthcare system.

The `Treatment` model tracks treatment details for patients, which can be associated with referral admissions.

Attributes:
    id (int): Unique identifier for the treatment record.
    name (str): The name of the treatment plan (e.g., 'Chemotherapy', 'Surgery').
    referral_admissions (list of `ReferralAdmission`): One-to-many relationship to referral admissions associated
    with this treatment plan.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.metrics import Base


class Treatment(Base):
    """
    Represents a type of treatment or intervention for a patient.

    Attributes:
        id (int): Primary key.
        name (str): Name of the treatment (e.g., 'Chemotherapy', 'Surgery').
        slot_bookings (list): Associated TreatmentSlotBooking records.
    """
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationship for slot bookings (reporting purposes)
    slot_bookings = relationship("TreatmentSlotBooking", back_populates="treatment")


class TreatmentSlotBooking(Base):
    """
    Represents a scheduled treatment slot.

    Attributes:
        id (int): Primary key.
        treatment_id (int): Foreign key to Treatment.
        patient_id (int): Optional foreign key to Patient.
        slot_time (datetime): Scheduled time for treatment.
    """
    __tablename__ = "treatment_slot_bookings"

    id = Column(Integer, primary_key=True, index=True)
    treatment_id = Column(Integer, ForeignKey("treatments.id"), nullable=False)
    patient_id = Column(Integer, nullable=True)
    slot_time = Column(DateTime, nullable=True)

    treatment = relationship("Treatment", back_populates="slot_bookings")
