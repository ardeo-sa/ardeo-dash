from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class Identifiers(Base):
    __tablename__ = 'identifiers'

    subject_id = Column(Integer, ForeignKey('subject.subject_id'), primary_key=True, nullable=False)
    identifier = Column(String)
    context_id = Column(Integer, ForeignKey('identifier_context.context_id'), primary_key=True, nullable=False)
    subject = relationship('Subject')
    identifier_context = relationship('IdentifierContext')
