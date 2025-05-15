from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayForms(Base):
    __tablename__ = 'pathway_forms'

    pathway_form_id = Column(Integer, primary_key=True, nullable=False)
    displayName = Column(String, nullable=False)
    filterFormId = Column(Integer, nullable=False)
    groupName = Column(String)
    isMandatory = Column(String)
