from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ReportingExportHistory(Base):
    __tablename__ = 'reporting_export_history'

    reporting_export_id = Column(Integer, primary_key=True, nullable=False)
    end_time = Column(DateTime)
    status_code = Column(Integer)
    start_time = Column(DateTime)
    started_by_username = Column(String)
