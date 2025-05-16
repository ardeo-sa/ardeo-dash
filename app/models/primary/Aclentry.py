from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Aclentry(Base):
    __tablename__ = 'aclentry'

    aclentry_id = Column(Integer, primary_key=True, nullable=False)
    aclentry_level = Column(Integer, nullable=False)
    acl = Column(Integer, ForeignKey('acl.acl_id'))
    aclentry_principalId = Column(Integer, ForeignKey('principal.principal_id'))
    aclentry_aclId = Column(Integer, ForeignKey('acl.acl_id'))
    acl = relationship('Acl')
    principal = relationship('Principal')
