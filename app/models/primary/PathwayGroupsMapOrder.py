from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class PathwayGroupsMapOrder(Base):
    __tablename__ = 'pathway_groups_map_order'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    pathway_group_id = Column(Integer)
    groupMapOrder_KEY = Column(Integer, primary_key=True, nullable=False)
    pathway = relationship('Pathway')
