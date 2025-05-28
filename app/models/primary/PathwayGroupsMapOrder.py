from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class PathwayGroupsMapOrder(Base):
    __tablename__ = 'pathway_groups_map_order'
    __table_args__ = {'extend_existing': True}
    pathway_id = Column(Integer, ForeignKey('pathway.id'), primary_key=True, nullable=False)
    pathway_group_id = Column(Integer , ForeignKey('pathway_groups.pathway_group_id'), primary_key=True, )
    groupMapOrder_KEY = Column(Integer, primary_key=True, nullable=False)
    pathway = relationship('Pathway')
