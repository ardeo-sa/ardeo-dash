from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserSpeciality(Base):
    __tablename__ = 'user_speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    speciality_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
