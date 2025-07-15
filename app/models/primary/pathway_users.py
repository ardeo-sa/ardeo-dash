"""
Defines the model for linking users to organisation pathways with ordering support.
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base

class PathwayUsers(Base):
    """
        Represents the association between users and organisation pathways,
         allowing for the coordination and management of user roles within clinical pathways.
         This model is essential for assigning clinicians and staff to specific pathways,
          ensuring that they are informed and accountable for their roles.

        Attributes:
        organisation_pathway_id : int  Foreign key linking to the OrganisationPathways model, indicating the pathway
        associated with the organisation.
        user_id : int  Foreign key linking to the Users model, representing the user assigned to the pathway.
        child_index : int  Index used for ordering users within the pathway, ensuring a structured approach to user
        assignments.

        Relationships:
        organisation_pathways : Relationship with the OrganisationPathways model to access pathway details.
        users :  Relationship with the Users model to access user information.
    """
    __tablename__ = 'pathway_users'
    organisation_pathway_id = Column(Integer, ForeignKey('organisation_pathways.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    child_index = Column(Integer, primary_key=True, nullable=False)
    organisation_pathways = relationship('Organisation_pathways')
    users = relationship('Users')
