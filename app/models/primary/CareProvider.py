from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CareProvider(Base):
    __tablename__ = 'care_provider'

    id = Column(Integer, primary_key=True, nullable=False)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    allowContactDisplay = Column(String)
    city = Column(String)
    country = Column(String)
    county = Column(String)
    department = Column(String)
    job_title = Column(String)
    mobile_phone = Column(String)
    organisation_name = Column(String)
    personal_information_bio = Column(String)
    personal_url = Column(String)
    postcode = Column(String)
    preferred_contact = Column(String)
    qualification = Column(String)
    secretary_name = Column(String)
    work_phone = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
