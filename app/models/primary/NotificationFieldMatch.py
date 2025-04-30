from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class NotificationFieldMatch(Base):
    __tablename__ = 'notification_field_match'

    fldmtch_id = Column(Integer, primary_key=True, nullable=False)
    fieldLabel = Column(String)
    fldmtch_fldname = Column(String, nullable=False)
    fldmtch_op = Column(Integer, nullable=False)
    fldmtch_value = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('notification.notification_id'))
    child_index = Column(Integer)
    notification = relationship('Notification')
