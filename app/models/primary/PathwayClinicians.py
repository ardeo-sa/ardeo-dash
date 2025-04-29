from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayClinicians(Base):
    __tablename__ = 'pathway_clinicians'

    hospital_pathway_id = Column(Integer, ForeignKey('hospital_pathways.hospital_pathway_id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    hospital_pathways = relationship('Hospital_pathways')
    users = relationship('Users')
