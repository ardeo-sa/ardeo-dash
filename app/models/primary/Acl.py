from sqlalchemy import Column, Integer, String
from app.config import Base

class Acl(Base):
    __tablename__ = 'acl'

    acl_id = Column(Integer, primary_key=True, nullable=False)
    acl_name = Column(String, nullable=False)
    acl_ownername = Column(String, nullable=False)
