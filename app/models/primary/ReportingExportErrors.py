from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ReportingExportErrors(Base):
    __tablename__ = 'reporting_export_errors'

    parent_id = Column(Integer, ForeignKey('reporting_export_history.reporting_export_id'), primary_key=True, nullable=False)
    error_value = Column(String)
    error_key = Column(Integer, primary_key=True, nullable=False)
    reporting_export_history = relationship('Reporting_export_history')
