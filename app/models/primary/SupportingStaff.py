from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SupportingStaff(Base):
    __tablename__ = 'supporting_staff'

    senior_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    supporting_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    users = relationship('Users')
