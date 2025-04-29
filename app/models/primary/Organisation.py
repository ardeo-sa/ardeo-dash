from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Organisation(Base):
    __tablename__ = 'organisation'

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String)
    is_central_hub = Column(String)
    city = Column(String)
    creation_date = Column(DateTime, nullable=False)
    code = Column(String, nullable=False)
    description = Column(String)
    name = Column(String)
    modified_date = Column(DateTime, nullable=False)
    postcode = Column(String)
    hosts_virtual_mdm = Column(String)
    pas_context_id = Column(Integer, ForeignKey('pas_context.pas_context_id'))
    pas_context = relationship('Pas_context')
