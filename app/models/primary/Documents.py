from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship



class Documents(Base):
    """
    Represents metadata for documents stored within the system,
    capturing essential information about each document for efficient management and retrieval.
    Attributes:
    id : int  Unique identifier for the document.
    category : str Category or type of the document.
    comment_guid : str  Globally unique identifier for associated comments.
    filename : str Filename of the stored document.
    guid : str  Globally unique identifier for the document.
    note_guid : str  Globally unique identifier for associated notes.
    original_name : str Original name of the document before upload.
    subject_guid : str  Globally unique identifier for the subject related to the document.
    title : str Title of the document.
    upload_date : datetime   Date and time when the document was uploaded.
    user_id : int Identifier linking to the user who uploaded the document.

    Relationships:
    users : Relationship with the Users model to link user-specific information.
    """
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
