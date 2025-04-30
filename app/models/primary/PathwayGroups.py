from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PathwayGroups(Base):
    __tablename__ = 'pathway_groups'

    pathway_group_id = Column(Integer, primary_key=True, nullable=False)
    groupName = Column(String, nullable=False)
    isSystem = Column(String, nullable=False)
