from sqlalchemy import Column, Integer, String
from app.config import Base

class SubjectNotes(Base):
    """
    Stores notes associated with subjects (patients), providing a mechanism for
    recording observations, assessments, and other relevant information.
    This model allows for flexible note-taking and supports different types of notes.

    Attributes:
    id : int Unique identifier for the note.
    note_type : int Integer code representing the type of note (e.g., assessment, progress, medication).  You'll likely need a separate lookup table to map these codes to human-readable descriptions.
    notes : str The actual note text.
    subject_id : intForeign key referencing the subject (patient) this note is associated with.

    """
    __tablename__ = 'subject_notes'

    id = Column(Integer, primary_key=True, nullable=False)
    note_type = Column(Integer, nullable=False)
    notes = Column(String)
    subject_id = Column(Integer, nullable=False)
