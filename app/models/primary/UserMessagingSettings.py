from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserMessagingSettings(Base):
    __tablename__ = 'user_messaging_settings'

    user_messaging_settings_id = Column(Integer, primary_key=True, nullable=False)
    isActive = Column(String, nullable=False)
    messaging_id = Column(Integer)
    preference = Column(String, nullable=False)
    type = Column(String, nullable=False)
    user_id = Column(Integer)
