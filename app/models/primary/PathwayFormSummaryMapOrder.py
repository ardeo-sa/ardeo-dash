from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class PathwayFormSummaryMapOrder(Base):
    __tablename__ = 'pathway_form_summary_map_order'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    pathway_form_summary_id = Column(Integer, ForeignKey('pathway_form_summary_map.pathway_FormSummary_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    pathway = relationship('Pathway')
    pathway_form_summary_map = relationship('Pathway_form_summary_map')
