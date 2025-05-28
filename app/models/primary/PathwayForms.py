from sqlalchemy import Column, Integer, String
from app.config import Base

class PathwayForms(Base):
    __tablename__ = 'pathway_forms'
    pathway_form_id = Column(Integer, primary_key=True, nullable=False)
    display_name = Column(String, nullable=False)
    afobject_id = Column(Integer, nullable=False)
    group_name = Column(String)
    is_mandatory = Column(String)
