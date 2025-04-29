from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class QueryBuilder(Base):
    __tablename__ = 'query_builder'

    query_id = Column(Integer, primary_key=True, nullable=False)
    query_creationDate = Column(DateTime, nullable=False)
    query_desc = Column(String, nullable=False)
    query_formName = Column(String)
    query_show_header = Column(String)
    query_modifiedDate = Column(DateTime, nullable=False)
    query_patient = Column(String)
    query_records = Column(String)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
