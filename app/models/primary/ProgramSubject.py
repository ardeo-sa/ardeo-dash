from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class ProgramSubject(Base):
    """
    Represents the association between programs and subjects (patients), allowing for the
    coordination and management of program participants within the healthcare system.
     This model is essential for tracking which subjects are enrolled in specific programs,
     facilitating effective scheduling and resource allocation.

    Attributes:
    program_id : int  Foreign key linking to the Program model, identifying the associated program.
    subject_id : int Foreign key linking to the Subject model, representing the subject enrolled in the program.
    child_index : int Index used for ordering subjects within the program, ensuring a structured approach to participant management.

    Relationships:
    program :  Relationship with the Program model to access program details.
    subject : Relationship with the Subject model to access subject information.
    """
    __tablename__ = 'program_subject'

    program_id = Column(Integer, ForeignKey('program.program_id'), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    program = relationship('Program')
    subject = relationship('Subject')
