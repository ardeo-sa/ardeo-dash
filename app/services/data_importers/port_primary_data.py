"""
Migrates data from the primary database to the metrics database.

This function handles the end-to-end process of fetching relevant data
from the primary database and inserting or updating it into the metrics
database to ensure synchronized reporting and analytics.
"""
import logging

from app.database.metrics import MetricsSessionLocal
from app.database.primary import PrimarySessionLocal
from app.services.data_importers.clinician_import_service import ClinicianImportService
from app.services.data_importers.mdt_import_service import MdtImportService
from app.services.data_importers.organisation_import_service import OrganisationImportService
from app.services.data_importers.pathway_import_service import PathwayImportService
from app.services.data_importers.patient_import_service import PatientImportService

logger = logging.getLogger(__name__)

def port_primary_data():
    """
        Migrates data from the primary database to the metrics database.

        This function orchestrates the data migration process by initializing database sessions,
        then invoking import services to fetch and insert data from the primary system
        into the metrics system.
    """
    logger.info("Starting primary data porting process.")

    primary_session = PrimarySessionLocal()
    secondary_session = MetricsSessionLocal()

    try:
        logger.info("Importing MDT data.")
        mdt_import_service = MdtImportService(secondary_session)
        mdt_import_service.import_mdt()
        logger.info("MDT data import completed.")

        logger.info("Importing clinician data.")
        clinician_import_service = ClinicianImportService(primary_session, secondary_session)
        clinician_import_service.import_clinician()
        logger.info("Clinician data import completed.")

        logger.info("Importing organisation data.")
        organisation_import_service = OrganisationImportService(primary_session, secondary_session)
        organisation_import_service.import_organisation()
        logger.info("Organisation data import completed.")

        logger.info("Importing pathway data.")
        pathway_import_service = PathwayImportService(primary_session, secondary_session)
        pathway_import_service.import_pathway()
        logger.info("Pathway data import completed.")

        logger.info("Importing patient and referral data.")
        patient_import_service = PatientImportService(primary_session, secondary_session)
        patient_import_service.import_patients_and_referrals()
        logger.info("Patient and referral data import completed.")

        logger.info("Primary data porting process completed successfully.")

    except Exception:
        logger.exception("An error occurred during the primary data porting process.")
        raise

    finally:
        primary_session.close()
        secondary_session.close()
        logger.info("Database sessions closed.")