from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayFormMap(Base):
    __tablename__ = 'pathway_form_map'

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    Form_name = Column(String)
    formsSet_KEY = Column(Integer, ForeignKey('pathway_forms.pathway_form_id'), primary_key=True, nullable=False)
    pathway = relationship('Pathway')
    pathway_forms = relationship('Pathway_forms')
