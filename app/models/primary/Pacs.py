from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Pacs(Base):
    __tablename__ = 'pacs'

    id = Column(Integer, primary_key=True, nullable=False)
    aet = Column(String)
    description = Column(String)
    enabled = Column(String)
    ip = Column(String)
    name = Column(String)
    port = Column(String)
