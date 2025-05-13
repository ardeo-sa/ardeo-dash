from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class GpList(Base):
    __tablename__ = 'gp_list'

    GPNo = Column(String, primary_key=True, nullable=False)
    Health_Centre_or_Road = Column(String)
    Town_or_City = Column(String)
    County = Column(String)
    gpAddress4 = Column(String)
    gpEmailAddress = Column(String)
    gpFaxNumber = Column(String)
    Initial = Column(String)
    gpPctCode = Column(String)
    gpPctName = Column(String)
    gpPostcode = Column(String)
    gpPracticeCode = Column(String)
    gpPracticeName = Column(String)
    Name = Column(String)
    Phone = Column(String)
