from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notification'

    notification_id = Column(Integer, primary_key=True, nullable=False)
    notification_creation_date = Column(DateTime, nullable=False)
    notification_desc = Column(String, nullable=False)
    notification_formName = Column(String)
    notification_modified_date = Column(DateTime, nullable=False)
    summary_id = Column(Integer)
    owner_id = Column(Integer, ForeignKey('notification_message.ntfnmsg_id'))
    notification_message = relationship('Notification_message')
