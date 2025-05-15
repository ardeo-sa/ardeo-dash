from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayUsers(Base):
    __tablename__ = 'pathway_users'

    organisation_pathway_id = Column(Integer, ForeignKey('organisation_pathways.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    organisation_pathways = relationship('Organisation_pathways')
    users = relationship('Users')
