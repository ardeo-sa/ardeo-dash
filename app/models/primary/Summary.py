from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Summary(Base):
    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True, nullable=False)
    backgroundColor = Column(String)
    description = Column(String)
    guid = Column(String, nullable=False)
    title = Column(String)
    createdBy_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
