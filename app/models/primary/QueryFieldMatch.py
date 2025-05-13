from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class QueryFieldMatch(Base):
    __tablename__ = 'query_field_match'

    qfldmtch_id = Column(Integer, primary_key=True, nullable=False)
    qfldmtch_fldname = Column(String, nullable=False)
    qfldmtch_fldparentname = Column(String)
    qfldmtch_inner_logical_opr = Column(String)
    qfldmtch_op = Column(Integer, nullable=False)
    qfldmtch_outer_logical_opr = Column(String)
    qfldmtch_out = Column(Integer)
    qfldmtch_sort_by_order = Column(String)
    qfldmtch_value = Column(String)
    owner_id = Column(Integer, ForeignKey('query_builder.query_id'))
    child_index = Column(Integer)
    query_builder = relationship('Query_builder')
