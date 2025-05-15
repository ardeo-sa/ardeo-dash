from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Clinic(Base):
    __tablename__ = 'clinic'

    clinic_id = Column(Integer, primary_key=True, nullable=False)
    clinic_group_code = Column(String, nullable=False)
    clinic_date = Column(DateTime)
    consultant_code = Column(String)
    consultant_forename = Column(String)
    consultant_surname = Column(String)
    institution_code = Column(String)
    speciality = Column(String, nullable=False)
