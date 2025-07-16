"""
Module defining ACL principal models and their relationships.

This module contains the base class AclPrincipal and its polymorphic subclasses
AclGroup and AclRole, which represent groups and roles in the access control system.
It also includes association models (GroupUsername and RoleUsername) linking users
to groups and roles respectively.

The polymorphic design enables flexible management of different types of principals
within the same access control framework.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base


class AclPrincipal(Base):
    """ Base class for defining access control principals in the application.
    This model serves as the root for polymorphic identity, enabling different types
    of principals like groups and roles.
    Attributes:
    ----------
    id : int A unique identifier for the principal.
    name : str The name of the principal.
    principal_id : str  A unique identifier for distinguishing different principals.
    principal_type : str  The type of the principal, used for polymorphic differentiation.
      Polymorphism:
    -------------
    This model uses polymorphic inheritance to allow different types of principals,
    such as groups and roles, to share a common interface while handling specific behaviors.
    """

    __tablename__ = 'principal'
    __mapper_args__ = {
        'polymorphic_on': 'principal_type',
        'polymorphic_identity': 'base',
        'with_polymorphic': '*'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String)
    principal_id = Column(String)
    principal_type = Column(String)

class AclGroup(AclPrincipal):

    """  Inherits from AclPrincipal to define a group of users within the access control system.
    Groups can contain multiple users and facilitate group-based permission management.
    Attributes:  Inherits all attributes from AclPrincipal.
    Relationships: members : relationship
        A one-to-many relationship with the GroupUsername model, representing users associated with this group.
    """
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }
    members = relationship(
        'GroupUsername',
        cascade='all, delete-orphan',
        backref='group'
    )

class GroupUsername(Base):
    """ Represents the association between a group and a username in the access control system.
    Attributes: group_id : int Foreign key linking to AclPrincipal's id for group associations.
                username : str The username of the user within the group.
    """
    __tablename__ = 'group_usernames'
    group_id = Column(Integer, ForeignKey('principal.id'), primary_key=True)
    username = Column(String, primary_key=True)

class AclRole(AclPrincipal):
    """
     Inherits from AclPrincipal to define a role within the access control system. Roles can contain multiple users and
     are used for role-based access management.
    Attributes: Inherits all attributes from AclPrincipal.
    Relationships: members : relationship A one-to-many relationship with the RoleUsername model, representing users
    associated with this role.
    """
    __mapper_args__ = {
        'polymorphic_identity': 'role',
    }

    members = relationship(
        'RoleUsername',
        cascade='all, delete-orphan',
        backref='role'
    )

class RoleUsername(Base):
    """
    Represents the association between a role and a username in the access control system.
    Attributes:  role_id : int Foreign key linking to AclPrincipal's id for role associations.
                username : str the username of the user within the role.
    """
    __tablename__ = 'role_usernames'

    role_id = Column(Integer, ForeignKey('principal.id'), primary_key=True)
    username = Column(String, primary_key=True)
