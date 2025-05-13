from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MdtList(Base):
    __tablename__ = 'mdt_list'

    mdt_list_id = Column(Integer, primary_key=True, nullable=False)
    mdt_list_name = Column(String, nullable=False)
    mdt_tumourGroup = Column(String)
