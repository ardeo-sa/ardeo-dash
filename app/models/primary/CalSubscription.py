from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CalSubscription(Base):
    __tablename__ = 'cal_subscription'

    type = Column(String, nullable=False)
    cs_id = Column(Integer, primary_key=True, nullable=False)
    cs_bgColour = Column(String)
    cs_enabled = Column(String, nullable=False)
    cs_fgColour = Column(String)
    cs_name = Column(String, nullable=False)
    cs_owner = Column(String)
    us_username = Column(String)
    gs_groupname = Column(String)
    ms_speciality = Column(String)
    parent_id = Column(Integer, ForeignKey('user_calendar.uc_id'))
    item_index = Column(Integer)
    user_calendar = relationship('User_calendar')
