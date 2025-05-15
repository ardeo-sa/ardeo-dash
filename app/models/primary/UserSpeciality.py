from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserSpeciality(Base):
    __tablename__ = 'user_speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    speciality_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
