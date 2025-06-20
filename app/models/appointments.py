"""
This module defines the `Appointment` model for tracking scheduled appointments
within the healthcare system.

Each appointment is linked to a patient and records key details such as whether
the appointment was attended or cancelled.
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Appointment(Base):
    """
        SQLAlchemy model representing a scheduled appointment for a patient.

        Attributes:
            id (int): Primary key for the appointment record.
            patient_id (int): Foreign key referencing the associated patient.
            scheduled_time (datetime): Date and time when the appointment is scheduled.
            attended (bool): Whether the patient attended the appointment.
            cancelled (bool): Whether the appointment was cancelled.
        Relationships:
            patient (Patient): The patient associated with the appointment.
            clinician (Clinician): The clinician handling the appointment, if applicable.
    """
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    scheduled_time = Column(DateTime)
    attended = Column(Boolean)
    cancelled = Column(Boolean)

    # Relationships
    patient = relationship('Patient', foreign_keys=[patient_id],back_populates="appointments")# Links to Patient model
    # clinician = relationship('Clinician', back_populates='appointments')  # If Clinician model exists

    def __repr__(self):
        return f"<Appointment(id={self.id}, patient_id={self.patient_id}, scheduled_time={self.scheduled_time})>"
