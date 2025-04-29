from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    accountNonExpired = Column(String, nullable=False)
    accountNonLocked = Column(String, nullable=False)
    user_can_edit = Column(String)
    creation_date = Column(DateTime)
    credentialsNonExpired = Column(String, nullable=False)
    dateAccountExpires = Column(DateTime)
    datePasswordLastChanged = Column(DateTime)
    deleted = Column(String)
    email = Column(String)
    email_verified = Column(String, nullable=False)
    enabled = Column(String, nullable=False)
    enforceStrongPassword = Column(String, nullable=False)
    external_ldap_user_id = Column(String)
    user_forename = Column(String)
    google_user = Column(String, nullable=False)
    guid = Column(String, nullable=False)
    isPatient = Column(String, nullable=False)
    ldap_user = Column(String, nullable=False)
    user_middlename = Column(String)
    modified_date = Column(DateTime)
    user_nickname = Column(String)
    password = Column(String, nullable=False)
    passwordCanExpire = Column(String)
    user_prefix = Column(String)
    profileImagePath = Column(String)
    secret = Column(String, nullable=False)
    user_suffix = Column(String)
    user_surname = Column(String)
    username = Column(String, nullable=False)
    using2FA = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey('organisation.id'))
    organisation = relationship('Organisation')
