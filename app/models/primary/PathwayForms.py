from sqlalchemy import Column, Integer, String
from app.config import Base

class PathwayForms(Base):
    """
    Represents the forms associated with a clinical pathway,
    defining the forms required for subject care processes.
     This model allows for the organization and management of forms within different pathways,
     ensuring that necessary documentation is completed during patient care.

    Attributes:
    pathway_form_id : int Unique identifier for the pathway form.
    display_name : str  User-friendly name of the form, displayed in the system.
    afobject_id : int  Identifier linking to the associated AFObject, representing the form's data structure.
    group_name : str Name of the group to which the form belongs, if applicable.
    is_mandatory : str  Flag indicating whether the form is mandatory ("Yes" or "No").

    """
    __tablename__ = 'pathway_forms'

    pathway_form_id = Column(Integer, primary_key=True, nullable=False)
    display_name = Column(String, nullable=False)
    afobject_id = Column(Integer, nullable=False)
    group_name = Column(String)
    is_mandatory = Column(String)
