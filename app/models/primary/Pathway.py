import uuid
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Association tables for ElementCollections (maps)
# Since you have maps with complex keys, in SQLAlchemy it's better to create separate tables.

pathway_form_map = Table(
    'pathway_form_map', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.pathway_id'), primary_key=True),
    Column('form_id', Integer, ForeignKey('pathway_forms.id'), primary_key=True),
    Column('form_name', String)  # The value in the Map
)

# For groupMap: Map<GroupForms, Boolean>
group_forms_map = Table(
    'pathway_groups_map', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.pathway_id'), primary_key=True),
    Column('group_form_id', Integer, ForeignKey('group_forms.id'), primary_key=True),
    Column('cant_be_empty', Boolean)
)

# For groupMapOrder: Map<Integer, Integer>
group_map_order = Table(
    'pathway_groups_map_order', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.pathway_id'), primary_key=True),
    Column('pathway_group_id', Integer, primary_key=True),
    Column('order_value', Integer)
)

pathway_summaries = Table(
    'pathway_summaries', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.pathway_id'), primary_key=True),
    Column('summary_id', Integer, ForeignKey('patient_summary.id'), primary_key=True),
    Column('summary_name', String)
)

# For formSummaryMapOrder: Many-to-many with order
pathway_formsummary_map_order = Table(
    'pathway_FormSummary_map_order', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.pathway_id'), primary_key=True),
    Column('form_summary_id', Integer, ForeignKey('form_summary_map_order.id'), primary_key=True),
    Column('child_index', Integer)
)

class Pathway(Base):
    __tablename__ = 'pathway'

    id = Column('pathway_id', Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    speciality = Column(String)
    order_index = Column('orderIndex', Integer)
    creation_date = Column('creation_date', DateTime, nullable=False, default=datetime.utcnow)
    modified_date = Column('modified_date', DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    guid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    is_inter_site_pathway = Column('isInterSitePathway', Boolean, nullable=False, default=False)
    inter_site_name = Column('interSiteName', String, nullable=False, default='local')
    description = Column(String(500))

    created_by_user_id = Column(Integer, ForeignKey('user.id'))
    modified_by_user_id = Column(Integer, ForeignKey('user.id'))

    created_by_user = relationship('Users', foreign_keys=[created_by_user_id], lazy='joined')
    modified_by_user = relationship('Users', foreign_keys=[modified_by_user_id], lazy='joined')

    hospital_pathways = relationship(
        'OrganisationPathways',
        backref='pathway',
        cascade='all, delete-orphan',
        lazy='subquery',
        passive_deletes=True,
        foreign_keys='OrganisationPathways.pathway_id'
    )

    # Relationships for collections (maps)
    forms_set = relationship(
        'PathwayForms',
        secondary=pathway_form_map,
        lazy='subquery'
    )

    group_map = relationship(
        'PathwayGroups',
        secondary=group_forms_map,
        lazy='subquery'
    )

    # For groupMapOrder and summaries and formSummaryMapOrder, you might want to map them explicitly.

    # This is just a rough placeholder to show usage:
    summaries = relationship(
        'Summary',
        secondary=pathway_summaries,
        lazy='subquery'
    )

    form_summary_map_order = relationship(
        'PathwayFormSummaryMapOrder',
        secondary=pathway_formsummary_map_order,
        order_by=pathway_formsummary_map_order.c.child_index,
        lazy='subquery'
    )

    def __repr__(self):
        return f"<Pathway(id={self.id}, title='{self.title}', guid={self.guid})>"

