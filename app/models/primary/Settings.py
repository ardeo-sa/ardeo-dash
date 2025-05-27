from sqlalchemy import Column, Integer, String
from app.config import Base



class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String)
    Property_key = Column(String, nullable=False)
    Property_value = Column(String)
