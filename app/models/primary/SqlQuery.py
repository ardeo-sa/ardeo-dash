from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SqlQuery(Base):
    __tablename__ = 'sql_query'

    id = Column(Integer, primary_key=True, nullable=False)
    query_creationDate = Column(DateTime, nullable=False)
    query_desc = Column(String, nullable=False)
    query_name = Column(String, nullable=False)
    query = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
