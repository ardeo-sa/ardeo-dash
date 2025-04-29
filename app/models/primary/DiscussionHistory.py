from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DiscussionHistory(Base):
    __tablename__ = 'discussion_history'

    id = Column(String, primary_key=True, nullable=False)
    commentDate = Column(DateTime, nullable=False)
    comments = Column(String, nullable=False)
    username = Column(String, nullable=False)
    thread_id = Column(String, ForeignKey('discussion.thread_id'))
    discussion = relationship('Discussion')
