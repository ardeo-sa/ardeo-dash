from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class NotificationMethod(Base):
    __tablename__ = 'notification_method'

    ntfm_id = Column(Integer, primary_key=True, nullable=False)
    ntfm_address = Column(String, nullable=False)
    ntfm_type = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('notification.notification_id'))
    notification = relationship('Notification')
