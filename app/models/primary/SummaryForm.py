from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SummaryForm(Base):
    __tablename__ = 'summary_form'

    id = Column(Integer, primary_key=True, nullable=False)
    afobject_id = Column(Integer)
    summary_id = Column(Integer, ForeignKey('summary.id'))
    item_index = Column(Integer)
    summary = relationship('Summary')
