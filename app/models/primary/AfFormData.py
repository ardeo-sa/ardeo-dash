from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AfFormData(Base):
    __tablename__ = 'af_form_data'

    af_type = Column(String, nullable=False)
    af_id = Column(Integer, primary_key=True, nullable=False)
    creation_date = Column(DateTime)
    deleted = Column(String)
    editable = Column(String)
    afobject_id = Column(Integer)
    guid = Column(String, nullable=False)
    modified_date = Column(DateTime)
    xml = Column(String)
    carespell_id = Column(Integer)
    locked = Column(String)
    locked_by = Column(String)
    locked_date = Column(DateTime)
    referral_id = Column(Integer)
    created_user = Column(Integer, ForeignKey('users.user_id'))
    modified_user = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
