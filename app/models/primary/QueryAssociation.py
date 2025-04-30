from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class QueryAssociation(Base):
    __tablename__ = 'query_association'

    rec_num = Column(Integer, primary_key=True, nullable=False)
    creation_date = Column(DateTime)
    query_id = Column(Integer)
    query_name = Column(String)
    template_name = Column(String)
