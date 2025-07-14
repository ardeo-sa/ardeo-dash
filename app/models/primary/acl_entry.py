"""
Module defining the Aclentry ORM model.

This module contains the SQLAlchemy model for ACL entries, which assign permission
levels to principals (users or groups) within a specific Access Control List (ACL).
Each entry links to both the ACL resource and the principal entity.
"""

from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class Aclentry(Base):
    """
       ORM model representing an ACL entry that defines permissions for a principal.

       An AclEntry associates an AclPrincipal (such as a user or group) with a specific
       permission level within an ACL. It links to both the ACL and the principal entities.

       Attributes:
           aclentry_id (int): Primary key for the ACL entry.
           aclentry_level (int): Permission level assigned (e.g., read, write).
           acl (int): Foreign key referencing the ACL this entry belongs to.
           aclentry_principalId (int): Foreign key referencing the principal (user or group).
           aclentry_aclId (int): Foreign key referencing the related ACL resource.
           aclrelation (Acl): Relationship to the associated ACL.
           principal (Principal): Relationship to the principal granted permissions.
       """
    __tablename__ = 'aclentry'

    aclentry_id = Column(Integer, primary_key=True, nullable=False)
    aclentry_level = Column(Integer, nullable=False)
    acl = Column(Integer, ForeignKey('acl.acl_id'))
    aclentry_principalId = Column(Integer, ForeignKey('principal.principal_id'))
    aclentry_aclId = Column(Integer, ForeignKey('aclrelation.acl_id'))
    aclrelation = relationship('Acl')
    principal = relationship('Principal')
