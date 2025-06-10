from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class SummaryForm(Base):
    """
     Represents a summary record, providing a mechanism for storing and managing
     concise overviews of information from form-definition.  This model is useful for
     capturing key details or conclusions, often used in conjunction with more detailed records.

    Attributes:
    id : intUnique identifier for the summary.
    backgroundColor : str Background color for display purposes (e.g., for UI rendering).
    description : str Detailed description of the summary's content.
    guid : strGlobally unique identifier for the summary.
    title : strConcise title or heading for the summary.
    createdBy_id : int Foreign key linking to the Users model, identifying the user who created the summary.

    Relationships:
    users : Relationship with the Users model to access creator details.
    """
    __tablename__ = 'summary_form'

    id = Column(Integer, primary_key=True, nullable=False)
    afobject_id = Column(Integer)
    summary_id = Column(Integer, ForeignKey('summary.id'))
    item_index = Column(Integer)
    summary = relationship('Summary')
