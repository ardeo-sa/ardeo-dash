from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProgramSubject(Base):
    __tablename__ = 'program_subject'

    program_id = Column(Integer, ForeignKey('program.program_id'), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    program = relationship('Program')
    subject = relationship('Subject')
