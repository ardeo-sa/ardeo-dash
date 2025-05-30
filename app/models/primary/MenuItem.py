from sqlalchemy import Column, Integer, String
from app.config import Base



class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String)
    description = Column(String)
    name = Column(String, nullable=False)
    published = Column(String)
