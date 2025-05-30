from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.ext.orderinglist import ordering_list

from app.config import Base
from sqlalchemy.orm import relationship

pathway_clinicians = Table(
    'pathway_users',
    Base.metadata,
    Column('organisation_pathway_id', Integer, ForeignKey('organisation_pathways.id'), nullable=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
    Column('child_index', Integer),  # Used for ordering
    UniqueConstraint('organisation_pathway_id', 'user_id', name='uq_pathway_user')
)

class OrganisationPathways(Base):
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