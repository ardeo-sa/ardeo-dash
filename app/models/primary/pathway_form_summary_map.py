"""
Represents the mapping between forms and summaries within a clinical pathway,
providing a structured approach to manage and organize forms and summaries
for effective patient care coordination.

Attributes:
-----------
pathway_form_summary_id : int
    Unique identifier for the mapping entry.
afobject_id : int
    Identifier linking to the associated AFObject, representing the data structure of the form or summary.
form_or_summary_name : str
    Name of the form or summary, providing a descriptive label.
group_name : str
    Name of the group to which the form or summary belongs.
location : int
    Location identifier indicating where the form or summary is used within the pathway.
name : str
    Name of the mapping entry, used for identification.
summary_id : int
    Identifier for the summary, if applicable.
type : str
    Type of the entry, distinguishing between forms and summaries.
"""

from sqlalchemy import Column, Integer, String

from app.config import Base

class PathwayFormSummaryMap(Base):
    """
    Represents the mapping between forms and summaries within a clinical pathway,
    providing a structured approach to manage and organize forms and summaries
    for effective patient care coordination.

    Attributes:
    pathway_form_summary_id : int Unique identifier for the mapping entry.
    afobject_id : int Identifier linking to the associated AFObject, representing the data structure
    of the form or summary.
    form_or_summary_name : str  Name of the form or summary, providing a descriptive label.
    group_name : str Name of the group to which the form or summary belongs.
    location : int Location identifier indicating where the form or summary is used within the pathway.
    name : str Name of the mapping entry, used for identification.
    summary_id : int Identifier for the summary, if applicable.
    type : str Type of the entry, distinguishing between forms and summaries.

    """
    __tablename__ = 'pathway_form_summary_map'

    pathway_form_summary_id = Column(Integer, primary_key=True, nullable=False)
    afobject_id = Column(Integer)
    form_or_summary_name = Column(String)
    group_name = Column(String, nullable=False)
    location = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    summary_id = Column(Integer)
    type = Column(String, nullable=False)
