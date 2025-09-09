"""
Defines the LabTestOrder model used to represent laboratory test requests
like blood work, urine analysis, or other diagnostic tests.

The model includes details such as the patient, test name, status, and
date of order. It plays a key role in managing clinical investigations
and monitoring test workflows.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base


class LabTestOrder(Base):
    """
    Represents a lab test order for a patient, including blood work or other diagnostics.

    Attributes:
        id (int): Primary key.
        subject_id (int): Foreign key to the patient/subject.
        test_name (str): Name of the test (e.g., 'CBC', 'LFT').
        status (str): Status of the test (e.g., 'pending', 'completed').
        order_date (datetime): Date when the test was ordered.

    Relationships:
        subject: Relationship to the Subject model.
    """
    __tablename__ = "lab_test_order"

    id = Column(Integer, primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), nullable=False)
    test_name = Column(String, nullable=False)
    status = Column(String, default="pending")
    order_date = Column(DateTime, nullable=False)

    subject = relationship("Subject", backref="lab_test_orders")
