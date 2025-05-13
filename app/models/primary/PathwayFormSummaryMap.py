from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayFormSummaryMap(Base):
    __tablename__ = 'pathway_form_summary_map'

    pathway_FormSummary_id = Column(Integer, primary_key=True, nullable=False)
    filterFormId = Column(Integer)
    formOrSummaryName = Column(String)
    groupName = Column(String, nullable=False)
    location = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    summaryId = Column(Integer)
    type = Column(String, nullable=False)
