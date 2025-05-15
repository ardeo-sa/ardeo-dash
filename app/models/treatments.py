"""
This module defines database models related to treatment plans and scheduling,
including available treatments and slot bookings by patients.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.metrics import Base


class Treatment(Base):
    """
    Represents a type of treatment or intervention that a patient may undergo.
    """
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    referral_admissions = relationship('ReferralAdmission', back_populates='treatment_plan')
    slot_bookings = relationship('TreatmentSlotBooking', back_populates='treatment')


class TreatmentSlotBooking(Base):
    """
    Represents a scheduled treatment slot assigned to a patient.

    Fields:
        - id: unique ID of the booking
        - treatment_id: FK to the treatment being scheduled
        - patient_id: ID of the patient (foreign key assumed elsewhere)
        - slot_time: datetime when the treatment is scheduled
    """
    __tablename__ = "treatment_slot_bookings"

    id = Column(Integer, primary_key=True)
    treatment_id = Column(Integer, ForeignKey("treatments.id"))
    patient_id = Column(Integer)  # optionally add FK to patient table if needed
    slot_time = Column(DateTime)

    treatment = relationship("Treatment", back_populates="slot_bookings")
