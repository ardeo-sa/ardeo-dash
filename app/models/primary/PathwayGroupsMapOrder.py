from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayGroupsMapOrder(Base):
    __tablename__ = 'pathway_groups_map_order'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    pathway_group_id = Column(Integer)
    groupMapOrder_KEY = Column(Integer, primary_key=True, nullable=False)
    pathway = relationship('Pathway')
