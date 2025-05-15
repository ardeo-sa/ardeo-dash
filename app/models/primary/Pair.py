from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Pair(Base):
    __tablename__ = 'pair'

    pair_id = Column(Integer, primary_key=True, nullable=False)
    nl_filter_org_code = Column(String)
    pair_first = Column(String, nullable=False)
    pair_second = Column(String, nullable=False)
    namedList_id = Column(Integer, ForeignKey('named_list.nl_id'))
    child_index = Column(Integer)
    named_list = relationship('Named_list')
