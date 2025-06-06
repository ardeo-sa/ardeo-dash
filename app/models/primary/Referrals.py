from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



class Referrals(Base):
    """
    Manages referral information within the healthcare system, tracking the details
    of referrals between different organisations, specialists, and pathways.
    This model is crucial for coordinating patient care and ensuring that referrals are
     processed efficiently and effectively.
    Attributes:
    referral_id : int  Unique identifier for the referral.
    acknowledgement_date : datetime Date and time when the referral was acknowledged.
    guid : str Globally unique identifier for the referral.
    image_transport : str  Method used for image transfer in the referral.
    manual_tracking : str  Flag indicating whether manual tracking is required ("Yes" or "No").
    registered : str  Flag indicating whether the referral has been registered ("Yes" or "No").
    referral_date : datetime Date and time when the referral was initiated.
    referral_method : int  Method used for referral.
    referral_mode : int Mode of referral.
    referral_notes : str Additional notes or comments on the referral.
    referral_status : int  Status of the referral (e.g., pending, completed).
    referring_from_organisation : int Identifier for the organisation initiating the referral.
    referring_specialist_address : str Address of the referring specialist.
    referring_specialist_fax : str   Fax number of the referring specialist.
    referring_specialist_org_code : str Organisational code of the referring specialist.
    referring_specialist_jobtitle : str Job title of the referring specialist.
    referring_specialist_name : str  Name of the referring specialist.
    referring_specialist_postcode : str  Postal code of the referring specialist.
    referring_specialist_telephone : str  Telephone number of the referring specialist.
    referring_specialist_username : str  Username of the referring specialist.
    referring_to_organisation : int dentifier for the organisation receiving the referral.
    response_date : datetime  Date and time when a response was received for the referral.
    team : str Team involved in the referral.
    tracking : str  Tracking information for the referral.
    episode_id : int  Foreign key linking to the Episode model.
    pathway_id : int Foreign key linking to the Pathway model.
    referred_from_user_id : int Foreign key linking to the Users model (user initiating the referral).
    referred_to_user_id : int  Foreign key linking to the Users model (user receiving the referral).
    referring_specialist_user_id : int Foreign key linking to the Users model (referring specialist).
    child_index : int  Index to manage multiple referrals for a single episode.

    Relationships:
    --------------
    episode :  Relationship with the Episode model.
    pathway :  Relationship with the Pathway model.
    referred_from_user :    Relationship with the Users model (user initiating the referral).
    referred_to_user :   Relationship with the Users model (user receiving the referral).
    referring_specialist_user :   Relationship with the Users model (referring specialist).

    """
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
    pathway_id = Column(Integer, ForeignKey('pathway.id'))
    referred_from_user_id = Column(Integer, ForeignKey('users.user_id'))
    referred_to_user_id = Column(Integer, ForeignKey('users.user_id'))
    referring_specialist_user_id = Column(Integer, ForeignKey('users.user_id'))
    child_index = Column(Integer)
    episode = relationship('Episode')
    pathway = relationship('Pathway')
    referred_from_user = relationship('Users', foreign_keys=[referred_from_user_id])
    referred_to_user =relationship('Users', foreign_keys=[referred_to_user_id])
    referring_specialist_user= relationship('Users',foreign_keys=[referring_specialist_user_id])

