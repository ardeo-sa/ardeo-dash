from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base

class AuditLog(Base):
    """
    Represents an audit log entry, capturing detailed records of actions performed within the application.
     This model is essential for tracking changes, user actions, and maintaining a history of events for auditing purposes.

    Attributes:
    audit_id : int Unique identifier for the audit log entry.
    audit_date : datetime  Date and time when the audit action took place.
    audit_form_id : int  Identifier for the form associated with the audit event.
    audit_module : str Name of the module where the audit event occurred.
    audit_result : str Result of the audit action (e.g., success, failure).
    audit_user_fullname : str Full name of the user who performed the action.
    audit_user_username : str  Username of the user who performed the action.
    audit_action_message : str Description of the action performed.
    subject_id : int  Identifier for the subject related to the audit event.
    audit_user_id : int Identifier for the user who performed the action.
    """
    __tablename__ = 'audit_log'

    audit_id = Column(Integer, primary_key=True, nullable=False)
    audit_date = Column(DateTime, nullable=False)
    audit_form_id = Column(Integer)
    audit_module = Column(String, nullable=False)
    audit_result = Column(String, nullable=False)
    audit_user_fullname = Column(String)
    audit_user_username = Column(String)
    audit_action_message = Column(String, nullable=False)
    subject_id = Column(Integer)
    audit_user_id = Column(Integer)
