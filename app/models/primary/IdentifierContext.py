from sqlalchemy import Column, Integer, String
from app.config import Base

class IdentifierContext(Base):
    __tablename__ = 'identifier_context'

    context_id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    name = Column(String)
