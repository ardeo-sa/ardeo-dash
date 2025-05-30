from sqlalchemy import Column, Integer
from app.config import Base



class UserSpeciality(Base):
    __tablename__ = 'user_speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    speciality_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
