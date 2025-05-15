from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CareProvider(Base):
    __tablename__ = 'care_provider'

    careProvider_id = Column(Integer, primary_key=True, nullable=False)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    allowContactDisplay = Column(String)
    city = Column(String)
    country = Column(String)
    county = Column(String)
    department = Column(String)
    jobTitle = Column(String)
    mobilePhone = Column(String)
    organisationName = Column(String)
    personalInformationBio = Column(String)
    personalUrl = Column(String)
    postCode = Column(String)
    preferredContact = Column(String)
    qualification = Column(String)
    secretaryName = Column(String)
    workPhone = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
