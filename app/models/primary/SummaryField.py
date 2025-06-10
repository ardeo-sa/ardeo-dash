from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class SummaryField(Base):
    """
     Represents a field within a summary form from form-fields, defining the individual components that make
     up a summary. This model allows for the structured creation and management of summary data,
     ensuring consistency and facilitating data analysis.

    Attributes:
    id : intUnique identifier for the summary field.
    field_name : str Name of the field, providing a user-friendly label.
    sfield_id : intForeign key referencing the `summary_form` table, linking this field to a specific summary form.
    item_index : intIndex used for ordering fields within the summary form.
    Relationships:
    summary_form : Relationship with the Summary_form model to access summary form details.
    """
    __tablename__ = 'summary_field'

    id = Column(Integer, primary_key=True, nullable=False)
    field_name = Column(String)
    sfield_id = Column(Integer, ForeignKey('summary_form.id'))
    item_index = Column(Integer)
    summary_form = relationship('Summary_form')
