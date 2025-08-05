"""
This module processes and aggregates data from the primary database.

It initializes services related to patient subjects and care pathways,
and then triggers metrics calculations for:

- Daily, weekly, and monthly admissions and discharges
- Average length of stay (ALOS)
- Pathway adherence rate
- Days to treatment

Note: This module is intended to be triggered as part of the main application
initialization and does not return or persist any values itself.
"""
import logging

from app.database.primary import PrimarySessionLocal
from app.services.data_processing.subject_service import SubjectService
from app.services.data_processing.pathway_service import PathwayService

logger = logging.getLogger(__name__)

def process_data():
    """
    Processes and aggregates admission and treatment-related data from the primary database.
    """
    try:
        with PrimarySessionLocal() as session:
            logger.debug("Primary database session opened")

            subject_service = SubjectService(session)
            logger.debug("SubjectService initialized")

            logger.info("Processing admissions and discharges by day")
            subject_service.admissions_discharges_by_day()

            logger.info("Processing admissions and discharges by week")
            subject_service.admissions_discharges_by_week()

            logger.info("Processing admissions and discharges by month")
            subject_service.admissions_discharges_by_month()

            logger.info("Calculating average length of stay (ALOS)")
            subject_service.average_length_of_stay()

            pathway_service = PathwayService(session)
            logger.debug("PathwayService initialized")

            logger.info("Calculating pathway adherence rate")
            pathway_service.pathway_adherence_rate()

            logger.info("Calculating days to treatment")
            pathway_service.days_to_treatment()

        logger.info("Primary data processing complete")

    except Exception as e:
        logger.exception(f"Error occurred during primary data processing: {e}")