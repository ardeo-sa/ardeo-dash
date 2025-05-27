from sqlalchemy import Column, Integer, String
from app.config import Base

class PathwayGroups(Base):
    __tablename__ = 'pathway_groups'

    pathway_group_id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String, nullable=False)
    is_system = Column(String, nullable=False)
