from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MdtListAttendeeDetails(Base):
    __tablename__ = 'mdt_list_attendee_details'

    mdt_list_attendee_id = Column(Integer, primary_key=True, nullable=False)
    mdt_list_attendee_fax = Column(String)
    mdt_list_attendee_letter = Column(String)
    mdt_list_attendee_telephone = Column(String)
    mdt_list_attendee_use = Column(String, nullable=False)
    mdt_list_attendee_User_id = Column(Integer, ForeignKey('users.user_id'))
    mdt_list_id = Column(Integer, ForeignKey('mdt_list.mdt_list_id'), nullable=False)
    users = relationship('Users')
    mdt_list = relationship('Mdt_list')
