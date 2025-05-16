from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String)
    description = Column(String)
    name = Column(String, nullable=False)
    published = Column(String)
