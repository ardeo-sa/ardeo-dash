from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship

class NamedList(Base):
    """
    Represents a named list containing pairs of names and values,
    allowing for organized collections of items within specified domains.
     This model is useful for managing configurable lists
     that can be updated and maintained by users and used across the system .

    Attributes:
    ----------
    nl_id : int   Unique identifier for the named list.
    nl_creationDate : datetime Timestamp when the list was created.
    description : str Description of the list's purpose or contents.
    nl_domain : str Domain within which the list is applicable, ensuring context-specific usage.
    nl_modifiedDate : datetime   Timestamp of the last modification to the list.
    nl_name : str Name of the list, used for identification and reference.
    created_by_user : int   Foreign key linking to the user who created the list.
    modified_by_user : int  Foreign key linking to the user who last modified the list.

    Relationships:
    users : Relationship with the Users model to access user details related to creation and modification.
    """
    __tablename__ = 'named_list'

    nl_id = Column(Integer, primary_key=True, nullable=False)
    nl_creationDate = Column(DateTime)
    description = Column(String)
    nl_domain = Column(String, nullable=False)
    nl_modifiedDate = Column(DateTime)
    nl_name = Column(String, nullable=False)
    created_by_user = Column(Integer, ForeignKey('users.user_id'))
    modified_by_user = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
