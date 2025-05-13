from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class NotificationMessage(Base):
    __tablename__ = 'notification_message'

    ntfnmsg_type = Column(Integer, nullable=False)
    ntfnmsg_id = Column(Integer, primary_key=True, nullable=False)
    sem_body = Column(String)
    sem_subject = Column(String)
