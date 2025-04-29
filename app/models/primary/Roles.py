from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Roles(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String)
    is_desktop = Column(String)
    enabled = Column(String, nullable=False)
    value = Column(String, nullable=False)
