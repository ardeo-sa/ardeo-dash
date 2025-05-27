from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class PathwayGroupsMap(Base):
    __tablename__ = 'pathway_groups_map'
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    mandatory = Column(String)
    groupMap_KEY = Column(Integer, ForeignKey('pathway_groups.pathway_group_id'), primary_key=True, nullable=False)
    pathway = relationship('Pathway', back_populates="pathway_groups_map")
    pathway_groups = relationship('Pathway_groups')
