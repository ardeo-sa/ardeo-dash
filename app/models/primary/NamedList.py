from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



class NamedList(Base):
    __tablename__ = 'named_list'

    nl_id = Column(Integer, primary_key=True, nullable=False)
    nl_creationDate = Column(DateTime)
    description = Column(String)
    nl_domain = Column(String, nullable=False)
    nl_modifiedDate = Column(DateTime)
    nl_name = Column(String, nullable=False)
    created_by_user = Column(Integer, ForeignKey('users.user_id'))
    modified_by_user = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
