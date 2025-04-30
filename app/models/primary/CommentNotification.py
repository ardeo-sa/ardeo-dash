from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CommentNotification(Base):
    __tablename__ = 'comment_notification'

    comment_id = Column(Integer, ForeignKey('comment.comments_id'), primary_key=True, nullable=False)
    isAcknowledged = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    comment = relationship('Comment')
    users = relationship('Users')
