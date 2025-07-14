from sqlalchemy import Column, Integer, String
from app.config import Base



class FormSequence(Base):
    """
    Represents a sequence generator for forms,
    providing automated numbering and formatting for form identifiers.
    Attributes:

    id : int  Unique identifier for the form sequence.
    current_value : int  Current value of the sequence, which increments with each use.
    format_mask : str  Mask used to format the sequence output.
    increment : int Value by which the sequence increases each step.
    name : str Name of the sequence, used for identification and reference.
    prefix : str  Optional prefix to prepend to the sequence value.
    suffix : str Optional suffix to append to the sequence value.
   """
    __tablename__ = 'form_sequence'

    id = Column(Integer, primary_key=True, nullable=False)
    current_value = Column(Integer, nullable=False)
    format_mask = Column(String)
    increment = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    prefix = Column(String)
    suffix = Column(String)
