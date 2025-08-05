"""
Module defining the AclGroup ORM model.

This module includes the AclGroup class, representing an access control group
used for managing group-based permissions and user associations within the application.
"""
from sqlalchemy.orm import relationship

from app.config import Base

class AclGroup(Base):
    """ An access control group within the application.This model serves as a principal entity for managing group
    based permissions and access control, capable of containing multiple users.
    Attributes:
    __mapper_args__: dict Contains the polymorphic identity for this model, defining it as a 'group'.
    Relationships:
    members: relationship A one-to-many relationship with the GroupUsername model, representing the users associated
    with this group.Includes cascading data_processing for when a group is deleted. """

    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }

    members = relationship("GroupUsername", back_populates="group", cascade="all, delete-orphan")
