from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class PathwayFormMap(Base):
    __tablename__ = 'pathway_form_map'
    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'), primary_key=True, nullable=False)
    formsSet_KEY = Column(Integer, ForeignKey('pathway_forms.pathway_form_id'), primary_key=True, nullable=False)
    Form_name = Column(String)
    # Relationships
    pathway = relationship('Pathway', backref='pathway_form_maps')
    pathway_forms = relationship('PathwayForms', backref='pathway_form_maps')