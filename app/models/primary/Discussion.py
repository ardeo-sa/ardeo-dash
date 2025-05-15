from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Discussion(Base):
    __tablename__ = 'discussion'

    thread_id = Column(String, primary_key=True, nullable=False)
    dead_line = Column(DateTime)
    discussion_Topic = Column(String)
    end_date = Column(DateTime)
    patient_id = Column(Integer)
    posted_by = Column(String)
    posted_to = Column(String)
    start_date = Column(DateTime)
    status = Column(String)
