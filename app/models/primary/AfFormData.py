from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship
from app.models.primary.Users import Users
from app.models.primary.parser.AfFormDataValuesParser import parse_form_values



class AfFormData(Base):
    __tablename__ = 'af_form_data'

    af_type = Column(String, nullable=False)
    af_id = Column(Integer, primary_key=True, nullable=False)
    creation_date = Column(DateTime)
    deleted = Column(String)
    editable = Column(String)
    afo_id = Column(Integer)
    guid = Column(String, nullable=False)
    modified_date = Column(DateTime)
    xml = Column(String)
    episode_id = Column(Integer)
    locked = Column(String)
    locked_by = Column(String)
    locked_date = Column(DateTime)
    referral_id = Column(Integer)
    created_user = Column(Integer, ForeignKey('users.user_id'))
    modified_user = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')

    @property
    def values(self):
        return parse_form_values(self.xml)
