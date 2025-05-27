from sqlalchemy import Column, Integer, String
from app.config import Base



class SubjectNotes(Base):
    __tablename__ = 'subject_notes'

    id = Column(Integer, primary_key=True, nullable=False)
    note_type = Column(Integer, nullable=False)
    notes = Column(String)
    subject_id = Column(Integer, nullable=False)
