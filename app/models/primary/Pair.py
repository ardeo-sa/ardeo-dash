from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class Pair(Base):
    __tablename__ = 'pair'

    pair_id = Column(Integer, primary_key=True, nullable=False)
    nl_filter_org_code = Column(String)
    pair_first = Column(String, nullable=False)
    pair_second = Column(String, nullable=False)
    namedList_id = Column(Integer, ForeignKey('named_list.nl_id'))
    child_index = Column(Integer)
    named_list = relationship('Named_list')
