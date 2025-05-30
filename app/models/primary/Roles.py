from sqlalchemy import Column, Integer, String
from app.config import Base
from sqlalchemy.orm import relationship

# Define the association table FIRST
class Roles(Base):
     __tablename__ = 'roles'

     role_id = Column(Integer, primary_key=True, nullable=False)
     description = Column(String)
     is_desktop = Column(String)
     enabled = Column(String, nullable=False)
     value = Column(String, nullable=False)