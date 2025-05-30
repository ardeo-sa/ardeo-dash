from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import registry
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import composite
from sqlalchemy import event
from sqlalchemy.orm import with_polymorphic
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import subqueryload
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Enum
from sqlalchemy import select
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import registry
from app.config import Base
from sqlalchemy.orm import relationship, declarative_mixin, declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import polymorphic_union
from sqlalchemy.orm import synonym
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import composite
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict



class AclPrincipal(Base):
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
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }

    members = relationship(
        'GroupUsername',
        cascade='all, delete-orphan',
        backref='group'
    )

class GroupUsername(Base):
    __tablename__ = 'group_usernames'

    group_id = Column(Integer, ForeignKey('principal.id'), primary_key=True)
    username = Column(String, primary_key=True)

class AclRole(AclPrincipal):
    __mapper_args__ = {
        'polymorphic_identity': 'role',
    }

    members = relationship(
        'RoleUsername',
        cascade='all, delete-orphan',
        backref='role'
    )

class RoleUsername(Base):
    __tablename__ = 'role_usernames'

    role_id = Column(Integer, ForeignKey('principal.id'), primary_key=True)
    username = Column(String, primary_key=True)
