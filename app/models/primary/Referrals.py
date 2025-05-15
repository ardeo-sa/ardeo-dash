from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Referrals(Base):
    __tablename__ = 'referrals'

    referral_id = Column(Integer, primary_key=True, nullable=False)
    acknowledgement_date = Column(DateTime)
    guid = Column(String, nullable=False)
    image_transport = Column(String)
    manual_tracking = Column(String)
    registered = Column(String)
    referral_date = Column(DateTime)
    referral_method = Column(Integer)
    referral_mode = Column(Integer)
    referral_notes = Column(String)
    referral_status = Column(Integer, nullable=False)
    referring_from_hospital = Column(Integer, nullable=False)
    referring_specialist_address = Column(String)
    referring_specialist_fax = Column(String)
    referring_specialist_hospcode = Column(String)
    referring_specialist_jobtitle = Column(String)
    referring_specialist_name = Column(String)
    referring_specialist_postcode = Column(String)
    referring_specialist_telephone = Column(String)
    referring_specialist_username = Column(String)
    referring_to_hospital = Column(Integer)
    response_date = Column(DateTime)
    team = Column(String)
    tracking = Column(String)
    carespell_id = Column(Integer, ForeignKey('carespell.carespell_id'), nullable=False)
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'))
    referred_from_user_id = Column(Integer, ForeignKey('users.user_id'))
    referred_to_user_id = Column(Integer, ForeignKey('users.user_id'))
    referring_specialist_user_id = Column(Integer, ForeignKey('users.user_id'))
    referralDetails_index = Column(Integer)
    carespell = relationship('Carespell')
    pathway = relationship('Pathway')
    users = relationship('Users')
