from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class RoleUsernames(Base):
    __tablename__ = 'role_usernames'

    role_id = Column(Integer, ForeignKey('principal.principal_id'), nullable=False)
    username = Column(String)
    principal = relationship('Principal')
