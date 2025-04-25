from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from app.database.metrics import Base


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    scheduled_time = Column(DateTime)
    attended = Column(Boolean)
    cancelled = Column(Boolean)

