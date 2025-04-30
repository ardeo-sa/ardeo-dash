from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Table, DateTime
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Association tables
pathway_form_map = Table(
    'pathway_form_map', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathways.pathway_id')),
    Column('form_name', String)
)

pathway_groups_map = Table(
    'pathway_groups_map', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathways.pathway_id')),
    Column('cant_be_empty', Boolean)
)

pathway_groups_map_order = Table(
    'pathway_groups_map_order', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathways.pathway_id')),
    Column('pathway_group_id', Integer)
)

pathway_summaries = Table(
    'pathway_summaries', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathways.pathway_id')),
    Column('summary_name', String)
)

pathway_formsummary_map_order = Table(
    'pathway_FormSummary_map_order', Base.metadata,
    Column('pathway_id', Integer, ForeignKey('pathways.pathway_id')),
    Column('pathway_FormSummary_id', Integer, ForeignKey('pathway_FormSummary_Map.pathway_FormSummary_id'))
)

class ReferralsDefinition(Base):
    __tablename__ = 'pathways'
    pathway_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    speciality = Column(String)
    order_index = Column(Integer)
    creation_date = Column(DateTime,  nullable=False)
    modified_date = Column(DateTime, nullable=False)
    guid = Column(String, nullable=False)

    interSiteName = Column(String, nullable=False)
    isInterSitePathway = Column(String, nullable=False)
    description = Column(String)

    created_by_user_id = Column(Integer, ForeignKey('user.id'))
    modified_by_user_id = Column(Integer, ForeignKey('user.id'))

    created_by_user = Column(Integer, ForeignKey('users.user_id'))
    modified_by_user = Column(Integer, ForeignKey('users.user_id'))
    hospital_pathways = relationship("HospitalPathway", backref="referral", cascade="all, delete-orphan")
    form_summary_map_order = relationship("FormSummaryMapOrder", secondary=pathway_formsummary_map_order)


