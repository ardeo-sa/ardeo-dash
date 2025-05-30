from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class SummaryForm(Base):
    __tablename__ = 'summary_form'

    id = Column(Integer, primary_key=True, nullable=False)
    afobject_id = Column(Integer)
    summary_id = Column(Integer, ForeignKey('summary.id'))
    item_index = Column(Integer)
    summary = relationship('Summary')
