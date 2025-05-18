from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Program(Base):
    __tablename__ = 'program'

    program_id = Column(Integer, primary_key=True, nullable=False)
    program_group_code = Column(String, nullable=False)
    program_date = Column(DateTime)
    consultant_code = Column(String)
    consultant_forename = Column(String)
    consultant_surname = Column(String)
    institution_code = Column(String)
    speciality = Column(String, nullable=False)
