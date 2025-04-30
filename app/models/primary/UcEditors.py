from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UcEditors(Base):
    __tablename__ = 'uc_editors'

    uc_id = Column(Integer, ForeignKey('user_calendar.uc_id'), nullable=False)
    username = Column(String)
    user_calendar = relationship('User_calendar')
