from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ContactBase(Base):
    __tablename__ = 'contact_base'

    contact_id = Column(Integer, primary_key=True, nullable=False)
    contact_dept = Column(String)
    contact_asstName = Column(String)
    contact_mngrName = Column(String)
    contact_spseName = Column(String)
    contact_office = Column(String)
    contact_org = Column(String)
    contact_profession = Column(String)
