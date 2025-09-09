"""
Represents pathways associated with an organisation, facilitating the management of
clinical pathways and their assigned clinicians within the healthcare network.

Attributes:
----------
id : int
    Unique identifier for the organisation pathway.
guid : str
    Globally unique identifier for the pathway.
is_published : str
    Flag indicating whether the pathway is published ("Yes" or "No").
organisation_id : int
    Foreign key linking to the Organisation model.
pathway_id : int
    Foreign key linking to the Pathway model.

Relationships:
-------------
organisation : Organisation
    Relationship with the Organisation model to access organisational details.
pathway : Pathway
    Relationship with the Pathway model to access pathway details.
clinicians : list of Users
    List of clinicians associated with the pathway, ordered by `child_index`.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from app.config import Base

pathway_clinicians = Table(
    'pathway_users',
    Base.metadata,
    Column('organisation_pathway_id', Integer, ForeignKey('organisation_pathways.id'), nullable=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
    Column('child_index', Integer),  # Used for ordering
    UniqueConstraint('organisation_pathway_id', 'user_id', name='uq_pathway_user')
)

class OrganisationPathways(Base):
    """
    Represents pathways associated with an organisation, facilitating the management of
    clinical pathways and their assigned clinicians within the healthcare network.
    Attributes:
    id : int Unique identifier for the organisation pathway.
    guid : str  Globally unique identifier for the pathway.
    is_published : str  Flag indicating whether the pathway is published ("Yes" or "No").
    organisation_id : int  Foreign key linking to the Organisation model.
    pathway_id : int  Foreign key linking to the Pathway model.

    Relationships:
    organisation : Relationship with the Organisation model to access organisational details.
    pathway :  Relationship with the Pathway model to access pathway details.
    clinicians : List of clinicians associated with the pathway, ordered by `child_index`.

    """
    __tablename__ = 'organisation_pathways'

    id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    is_published = Column(String)
    organisation_id = Column(Integer, ForeignKey('organisation.id'))

    organisation = relationship('Organisation')
    pathway_id = Column(Integer, ForeignKey('pathway.id'))
    pathway = relationship('Pathway')
    clinicians = relationship(
        'Users',
        secondary='pathway_users',
        order_by='pathway_users.c.child_index', #.c attribute is a shorthand for accessing the columns of the table
        collection_class=ordering_list('child_index'),
        lazy='joined'
    )
