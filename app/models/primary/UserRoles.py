from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserRoles(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    users = relationship('Users')
    roles = relationship('Roles')
