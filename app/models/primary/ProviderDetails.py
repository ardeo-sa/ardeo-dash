from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



class ProviderDetails(Base):
    __tablename__ = 'provider_details'

    id = Column(Integer, primary_key=True, nullable=False)
    action_date = Column(DateTime)
    address = Column(String)
    country = Column(String)
    email_address = Column(String)
    full_name = Column(String)
    organisation_code = Column(String)
    organisation_name = Column(String)
    mobile_phone = Column(String)
    subject_identifier = Column(String)
    postcode = Column(String)
    role = Column(String)
    speciality = Column(String)
    username = Column(String)
    work_phone = Column(String)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    child_index = Column(Integer)
    subject = relationship('Subject')
