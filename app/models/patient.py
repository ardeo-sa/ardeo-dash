
from sqlalchemy import Column, Integer, String, Date, Float
from app.database.metrics import Base


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    admission_date = Column(Date)
    discharge_date = Column(Date)
