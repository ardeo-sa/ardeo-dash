from sqlalchemy import Column, Integer, String
from app.config import Base

class IdentifierContext(Base):
    """
     Represents a IdentifierContext or Master Subject Index,
     defining a logical namespace for Subject identifiers.
     This model ensures that Subject identifiers are unique within an associated organization
      or shared across multiple organization sites using the same physical Context.
    Attributes:
    context_id : int  Unique identifier for the identifier context, serving as the primary key.
    guid : str Globally unique identifier for the context.
    name : str  Name of the context, typically associated with a hospital or group of hospitals.

    """
    __tablename__ = 'identifier_context'

    context_id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    name = Column(String)
