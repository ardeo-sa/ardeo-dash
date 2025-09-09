"""
Module defining the SupportingStaff model used to represent hierarchical relationships
between senior and supporting staff within the organization.

This model is essential for managing reporting structures, facilitating team-based workflows,
and enabling permission or responsibility delegation in complex organizational settings.
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base


class SupportingStaff(Base):
    """
    Represents the relationship between senior staff and their supporting staff members,
    facilitating the management of teams and ensuring clear reporting structures within
    the organization. This model is crucial for defining and maintaining team hierarchies.

    Attributes:
    senior_staff_id : int   Foreign key referencing the `users` table, identifying the senior staff member.
    supporting_staff_id : int Foreign key referencing the `users` table, identifying the supporting staff member.

    Relationships:
    senior_staff : Relationship to access the senior staff user details.
    supporting_staff : Relationship to access the supporting staff user details.
    """
    __tablename__ = 'supporting_staff'

    senior_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    supporting_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)

    senior_staff = relationship('Users', foreign_keys=[senior_staff_id])
    supporting_staff = relationship('Users', foreign_keys=[supporting_staff_id])
