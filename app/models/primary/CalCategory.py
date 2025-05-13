from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CalCategory(Base):
    __tablename__ = 'cal_category'

    category_id = Column(Integer, primary_key=True, nullable=False)
    category_bgColour = Column(String)
    category_fgColour = Column(String)
    category_name = Column(String, nullable=False)
    category_owner = Column(String)
