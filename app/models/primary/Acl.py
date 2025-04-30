from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Acl(Base):
    __tablename__ = 'acl'

    acl_id = Column(Integer, primary_key=True, nullable=False)
    acl_name = Column(String, nullable=False)
    acl_ownername = Column(String, nullable=False)
