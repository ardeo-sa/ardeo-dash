from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



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
    referring_from_organisation = Column(Integer, nullable=False)
    referring_specialist_address = Column(String)
    referring_specialist_fax = Column(String)
    referring_specialist_org_code = Column(String)
    referring_specialist_jobtitle = Column(String)
    referring_specialist_name = Column(String)
    referring_specialist_postcode = Column(String)
    referring_specialist_telephone = Column(String)
    referring_specialist_username = Column(String)
    referring_to_organisation = Column(Integer)
    response_date = Column(DateTime)
    team = Column(String)
    tracking = Column(String)
    episode_id = Column(Integer, ForeignKey('episode.episode_id'), nullable=False)
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'))
    referred_from_user_id = Column(Integer, ForeignKey('users.user_id'))
    referred_to_user_id = Column(Integer, ForeignKey('users.user_id'))
    referring_specialist_user_id = Column(Integer, ForeignKey('users.user_id'))
    child_index = Column(Integer)
    episode = relationship('Episode')
    pathway = relationship('Pathway')
    users = relationship('Users')
