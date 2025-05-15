from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_log'

    auditId = Column(Integer, primary_key=True, nullable=False)
    audit_date = Column(DateTime, nullable=False)
    audit_form_id = Column(Integer)
    audit_module = Column(String, nullable=False)
    audit_result = Column(String, nullable=False)
    audit_user_fullname = Column(String)
    audit_user_username = Column(String)
    audit_action_message = Column(String, nullable=False)
    audit_patient_id = Column(Integer)
    audit_user_id = Column(Integer)
