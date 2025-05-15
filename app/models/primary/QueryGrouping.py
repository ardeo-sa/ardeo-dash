from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class QueryGrouping(Base):
    __tablename__ = 'query_grouping'

    id = Column(Integer, ForeignKey('query_builder.query_id'), primary_key=True, nullable=False)
    group_value = Column(String)
    groupingCodes_KEY = Column(String, primary_key=True, nullable=False)
    query_builder = relationship('Query_builder')
