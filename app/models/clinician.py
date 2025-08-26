"""
This module defines the `Clinician` and `ClinicianTask` models for storing
healthcare staff information and their associated tasks in the metrics database.

Clinicians are linked to referral admissions and tasks they are responsible for.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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
        tasks (List[ClinicianTask]): List of assigned tasks for the clinician.
    """
    __tablename__ = "clinician"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_role = Column(String)

    # Relationships
    referrals_made = relationship('ReferralAdmission', back_populates='referring_clinician',
                                  foreign_keys='ReferralAdmission.referring_clinician_id')
    referrals_received = relationship('ReferralAdmission', back_populates='receiving_clinician',
                                      foreign_keys='ReferralAdmission.receiving_clinician_id')
    tasks = relationship('ClinicianTask', back_populates='clinician')
    appointments = relationship('Appointment', back_populates='clinician')


class ClinicianTask(Base):
    """
    SQLAlchemy model representing tasks assigned to clinicians.

    Attributes:
        id (int): Primary key for the task.
        clinician_id (int): Foreign key referencing the assigned clinician.
        description (str): Description of the task.
        completed (bool): Whether the task has been completed.
    """
    __tablename__ = "clinician_task"

    id = Column(Integer, primary_key=True, index=True)
    clinician_id = Column(Integer, ForeignKey("clinician.id"), nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    # Relationships
    clinician = relationship('Clinician', back_populates='tasks')
