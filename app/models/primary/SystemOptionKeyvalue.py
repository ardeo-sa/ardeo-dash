from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SystemOptionKeyvalue(Base):
    __tablename__ = 'system_option_keyvalue'

    id = Column(Integer, primary_key=True, nullable=False)
    isActive = Column(String, nullable=False)
    description = Column(String)
    isEnabled = Column(String, nullable=False)
    FlagLevel = Column(String)
    system_key = Column(String, nullable=False)
