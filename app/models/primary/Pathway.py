import uuid
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship, foreign
from app.config import Base

# Association tables for ElementCollections (maps)
# Since you have maps with complex keys, in SQLAlchemy it's better to create separate tables.

# For formsSet: Map<ReferralsDefinitionForms, String>
# Assuming ReferralsDefinitionForms is another entity with id or name

pathway_form_map = Table(
    'pathway_form_map', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.id'), nullable=False),
    Column('formsSet_KEY', Integer, ForeignKey('pathway_forms.pathway_form_id'), nullable=False),
    Column('form_name', String)
)

pathway_groups_map = Table(
    'pathway_groups_map', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.id'), primary_key=True),
    Column('groupMap_KEY', Integer, ForeignKey('pathway_groups.pathway_group_id'), primary_key=True),
    Column('mandatory', Boolean)
)

group_map_order = Table(
    'pathway_groups_map_order', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.id'), primary_key=True),
    Column('pathway_group_id', Integer, ForeignKey('pathway_groups.pathway_group_id'), primary_key=True),
    Column('groupMapOrder_KEY', Integer)
)

pathway_summaries = Table(
    'pathway_summaries', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.id'), primary_key=True),
    Column('summaries_KEY', Integer, ForeignKey('summary.id'), primary_key=True),
    Column('summary_name', String),
)
pathway_formsummary_map_order = Table(
    'pathway_FormSummary_map_order', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathway.id'), primary_key=True),
    Column('pathway_form_summary_id', Integer, ForeignKey('pathway_form_summary_map.pathway_FormSummary_id'), primary_key=True),
    Column('child_index', Integer)
)

class Pathway(Base):
    __tablename__ = 'pathway'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    speciality = Column(String)
    order_index = Column('orderIndex', Integer)
    creation_date = Column('creation_date', DateTime, nullable=False, default=datetime.utcnow)
    modified_date = Column('modified_date', DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    guid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    is_inter_site_pathway = Column('isInterSitePathway', Boolean, nullable=False, default=False)
    inter_site_name = Column('interSiteName', String, nullable=False, default='local')
    description = Column(String(500))

    created_by_user_id = Column(Integer, ForeignKey('users.user_id'))
    modified_by_user_id = Column(Integer, ForeignKey('users.user_id'))

    created_by_user = relationship('Users', foreign_keys=[created_by_user_id], lazy='joined')
    modified_by_user = relationship('Users', foreign_keys=[modified_by_user_id], lazy='joined')

    # Relationships for collections (maps)\
    forms_set = relationship("PathwayForms", secondary=pathway_form_map, backref="pathway", lazy="subquery")  # eager fetching like FetchType.EAGER)
    group_map = relationship('PathwayGroups',secondary=pathway_groups_map,lazy='subquery')
    group_map_order = relationship('PathwayGroupsMapOrder', cascade='all, delete-orphan', back_populates='pathway')
    summaries = relationship('Summary',secondary=pathway_summaries,  backref="pathway", lazy='subquery')
    form_summary_map_order = relationship('PathwayFormSummaryMap', secondary=pathway_formsummary_map_order, order_by=pathway_formsummary_map_order.c.child_index, lazy='subquery')

    def __repr__(self):
        return f"<Pathway(id={self.id}, title='{self.title}', guid={self.guid})>"

