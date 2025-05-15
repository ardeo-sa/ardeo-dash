from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ReportingFrequency(Base):
    __tablename__ = 'reporting_frequency'

    activity_rep_freq_id = Column(Integer, primary_key=True, nullable=False)
    activity_report_name = Column(String)
    preferred_weekday = Column(String)
    preferred_frequency = Column(Integer)
    preferred_hour = Column(Integer)
    preferred_minutes = Column(Integer)
    EveryDay = Column(String)
    FriDay = Column(String)
    MonDay = Column(String)
    SaturDay = Column(String)
    SunDay = Column(String)
    ThursDay = Column(String)
    TuesDay = Column(String)
    WendsDay = Column(String)
    user_id = Column(Integer)
