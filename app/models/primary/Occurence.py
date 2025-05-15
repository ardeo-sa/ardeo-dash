from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Occurence(Base):
    __tablename__ = 'occurence'

    type = Column(String, nullable=False)
    occurence_id = Column(Integer, primary_key=True, nullable=False)
    occurence_endDate = Column(DateTime, nullable=False)
    guid = Column(String, nullable=False)
    occurence_resId = Column(String, nullable=False)
    occurence_startDate = Column(DateTime, nullable=False)
    occurence_title = Column(String, nullable=False)
    event_access = Column(Integer, nullable=False)
    event_category = Column(String)
    event_description = Column(String)
    event_externalReceivingUserEmails = Column(String)
    event_formurl = Column(String)
    event_location = Column(String)
    recur_byDay = Column(String)
    recur_byMonth = Column(String)
    recur_byMonthDay = Column(String)
    recur_byWeekNo = Column(String)
    recur_byYearDay = Column(String)
    recur_count = Column(String)
    recur_endType = Column(String)
    recur_frequency = Column(String)
    recur_interval = Column(String)
    recur_until = Column(String)
    event_recurrence = Column(String)
    event_reminder = Column(DateTime)
    event_useReminder = Column(String, nullable=False)
    event_status = Column(String, nullable=False)
