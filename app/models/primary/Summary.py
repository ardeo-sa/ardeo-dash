from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class Summary(Base):
    """
    Represents a summary record, providing a mechanism for storing and managing concise overviews
    of information.  This model is useful for capturing key details or conclusions,
     often used in conjunction with more detailed records.

    Attributes:
    id : int unique identifier for the summary.
    backgroundColor : str Background color for display purposes (e.g., for UI rendering).
    description : str  Detailed description of the summary's content.
    guid : str  Globally unique identifier for the summary.
    title : str Concise title or heading for the summary.
    createdBy_id : int Foreign key linking to the Users model, identifying the user who created the summary.
    Relationships:
    users :   Relationship with the Users model to access creator details.

    """
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True, nullable=False)
    backgroundColor = Column(String)
    description = Column(String)
    guid = Column(String, nullable=False)
    title = Column(String)
    createdBy_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
