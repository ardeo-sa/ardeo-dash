from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship

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
    context_id = Column(Integer, ForeignKey('identifier_context.context_id'))
    identifier_context = relationship('IdentifierContext')
