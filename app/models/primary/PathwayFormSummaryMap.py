from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PathwayFormSummaryMap(Base):
    __tablename__ = 'pathway_form_summary_map'

    pathway_FormSummary_id = Column(Integer, primary_key=True, nullable=False)
    afobject_id = Column(Integer)
    form_or_summary_name = Column(String)
    group_name = Column(String, nullable=False)
    location = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    summary_id = Column(Integer)
    type = Column(String, nullable=False)
