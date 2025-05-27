from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String)
    comment_guid = Column(String)
    filename = Column(String)
    guid = Column(String, nullable=False)
    note_guid = Column(String)
    original_name = Column(String)
    subject_guid = Column(String)
    title = Column(String)
    upload_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
