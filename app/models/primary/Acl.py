from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Acl(Base):
    __tablename__ = 'acl'

    acl_id = Column(Integer, primary_key=True, nullable=False)
    acl_name = Column(String, nullable=False)
    acl_ownername = Column(String, nullable=False)
