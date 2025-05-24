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
    Represents a type of treatment or intervention that a patient may undergo.
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
