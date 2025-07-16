"""
This module processes and aggregates operational data from the primary database.

It initializes services related to patient subjects and care pathways,
and then triggers metrics calculations for:

- Daily, weekly, and monthly admissions and discharges
- Average length of stay (ALOS)
- Pathway adherence rate
- Days to treatment

Note: This module is intended to be triggered as part of the main application
initialization and does not return or persist any values itself.
"""

from app.database.primary import PrimarySessionLocal
from app.services.operations.subject_service import SubjectService
from app.services.operations.pathway_service import PathwayService


def process_data():
    """
    Processes and aggregates admission and treatment-related data from the primary database.
    """
    with PrimarySessionLocal() as session:
        subject_service = SubjectService(session)
        subject_service.admissions_discharges_by_day()
        subject_service.admissions_discharges_by_week()
        subject_service.admissions_discharges_by_month()
        subject_service.average_length_of_stay()

        pathway_service = PathwayService(session)
        pathway_service.pathway_adherence_rate()
        pathway_service.days_to_treatment()
