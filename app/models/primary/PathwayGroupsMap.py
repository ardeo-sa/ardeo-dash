from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayGroupsMap(Base):
    __tablename__ = 'pathway_groups_map'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    cantBeEmpty = Column(String)
    groupMap_KEY = Column(Integer, ForeignKey('pathway_groups.pathway_group_id'), primary_key=True, nullable=False)
    pathway = relationship('Pathway')
    pathway_groups = relationship('Pathway_groups')
