from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayFormSummaryMapOrder(Base):
    __tablename__ = 'pathway_form_summary_map_order'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    pathway_FormSummary_id = Column(Integer, ForeignKey('pathway_form_summary_map.pathway_FormSummary_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    pathway = relationship('Pathway')
    pathway_form_summary_map = relationship('Pathway_form_summary_map')
