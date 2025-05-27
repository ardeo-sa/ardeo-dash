from sqlalchemy import Column, Integer, String
from app.config import Base



class Speciality(Base):
    __tablename__ = 'speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
