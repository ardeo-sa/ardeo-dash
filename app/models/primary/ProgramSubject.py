from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class ProgramSubject(Base):
    __tablename__ = 'program_subject'

    program_id = Column(Integer, ForeignKey('program.program_id'), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    program = relationship('Program')
    subject = relationship('Subject')
