from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Messaging(Base):
    __tablename__ = 'messaging'

    messaging_id = Column(Integer, primary_key=True, nullable=False)
    isActive = Column(String, nullable=False)
    allowAudioNotification = Column(String, nullable=False)
    messaging_description = Column(String)
    messaging_key = Column(String, nullable=False)
