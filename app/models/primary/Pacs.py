from sqlalchemy import Column, Integer, String
from app.config import Base



class Pacs(Base):
    __tablename__ = 'pacs'

    id = Column(Integer, primary_key=True, nullable=False)
    aet = Column(String)
    description = Column(String)
    enabled = Column(String)
    ip = Column(String)
    name = Column(String)
    port = Column(String)
