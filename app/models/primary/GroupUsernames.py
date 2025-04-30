from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class GroupUsernames(Base):
    __tablename__ = 'group_usernames'

    group_id = Column(Integer, ForeignKey('principal.principal_id'), nullable=False)
    username = Column(String)
    principal = relationship('Principal')
