"""
Defines the ImagingOrder model used to represent medical imaging orders
such as X-rays, MRIs, or CT scans.

This model links each imaging order to a patient (subject) and captures
important metadata such as order type, status, and date of request. It is
essential for tracking diagnostic imaging activity within the healthcare system.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base


class ImagingOrder(Base):
    """
    Represents an imaging order placed for a patient, such as X-ray, MRI, or CT scan.

    Attributes:
        id (int): Primary key.
        subject_id (int): Foreign key to the patient/subject.
        order_type (str): Type of imaging (e.g., 'X-Ray', 'MRI').
        status (str): Status of the order (e.g., 'ordered', 'completed').
        order_date (datetime): Date the imaging order was placed.

    Relationships:
        subject: Relationship to the Subject model.
    """
    __tablename__ = "imaging_order"

    id = Column(Integer, primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), nullable=False)
    order_type = Column(String, nullable=False)
    status = Column(String, default="ordered")
    order_date = Column(DateTime, nullable=False)

    subject = relationship("Subject", backref="imaging_orders")
