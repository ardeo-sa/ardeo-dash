from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class PathwaySummaries(Base):
    __tablename__ = 'pathway_summaries'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    summary_name = Column(String)
    summaries_KEY = Column(Integer, ForeignKey('summary.id'), primary_key=True, nullable=False)
    pathway = relationship('Pathway')
    summary = relationship('Summary')
