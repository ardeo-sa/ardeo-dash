from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class PathwayUsers(Base):
    __tablename__ = 'pathway_users'
    organisation_pathway_id = Column(Integer, ForeignKey('organisation_pathways.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    organisation_pathways = relationship('Organisation_pathways')
    users = relationship('Users')
