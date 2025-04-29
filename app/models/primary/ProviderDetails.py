from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProviderDetails(Base):
    __tablename__ = 'provider_details'

    id = Column(Integer, primary_key=True, nullable=False)
    action_date = Column(DateTime)
    address = Column(String)
    country = Column(String)
    email_address = Column(String)
    full_name = Column(String)
    hospital_code = Column(String)
    hospital_name = Column(String)
    mobile_phone_number = Column(String)
    patient_hospital_number = Column(String)
    postcode = Column(String)
    role = Column(String)
    speciality = Column(String)
    username = Column(String)
    work_phone_number = Column(String)
    patient_id = Column(Integer, ForeignKey('patient.patient_id'))
    pd_index = Column(Integer)
    patient = relationship('Patient')
