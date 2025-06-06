from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class SupportingStaff(Base):
    """
     Represents the relationship between senior staff and their supporting staff members,
     facilitating the management of teams and ensuring clear reporting structures within
     the organization. This model is crucial for defining and maintaining team hierarchies.

    Attributes:
    senior_staff_id : int   Foreign key referencing the `users` table, identifying the senior staff member.
    supporting_staff_id : int Foreign key referencing the `users` table, identifying the supporting staff member.

    Relationships:
    users :  This relationship allows accessing user details for both senior and supporting staff members.
    """
    _tablename__ = 'supporting_staff'

    senior_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    supporting_staff_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    users = relationship('Users')
