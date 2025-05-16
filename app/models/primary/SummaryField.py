from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SummaryField(Base):
    __tablename__ = 'summary_field'

    id = Column(Integer, primary_key=True, nullable=False)
    field_name = Column(String)
    sfield_id = Column(Integer, ForeignKey('summary_form.id'))
    item_index = Column(Integer)
    summary_form = relationship('Summary_form')
