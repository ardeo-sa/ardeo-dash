from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class SupportingStaff(Base):
    __tablename__ = 'supporting_staff'

    senior_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    supporting_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    users = relationship('Users')
