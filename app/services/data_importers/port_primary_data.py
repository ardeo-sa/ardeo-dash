"""
Migrates data from the primary database to the metrics database.

This function handles the end-to-end process of fetching relevant data
from the primary database and inserting or updating it into the metrics
database to ensure synchronized reporting and analytics.
"""
from app.database.metrics import MetricsSessionLocal
from app.database.primary import PrimarySessionLocal
# from app.services.data_importers.clinician_import_service import ClinicianImportService
from app.services.data_importers.mdt_import_service import MdtImportService
# from app.services.data_importers.organisation_import_service import OrganisationImportService
# from app.services.data_importers.pathway_import_service import PathwayImportService
# from app.services.data_importers.patient_import_service import PatientImportService

def portprimarydata():
    """
        Migrates data from the primary database to the metrics database.

        This function orchestrates the data migration process by initializing database sessions,
        then invoking import services to fetch and insert data from the primary system
        into the metrics system. Currently, only MDT data import is active.

        Uncommented import services (clinician, organisation, pathway, patient) can be enabled
        to extend the migration process as needed.
    """
    PrimarySessionLocal()
    secondary_session = MetricsSessionLocal()

    mdt_import_service = MdtImportService(secondary_session)
    mdt_import_service.import_mdt()

    #
    # clinicianImportService = ClinicianImportService(primary_session,secondary_session)
    # clinicianImportService.import_clinician()
    #
    # organisationsImportService = OrganisationImportService(primary_session, secondary_session)
    # organisationsImportService.import_organisation()
    #
    # pathwayImportService = PathwayImportService(primary_session, secondary_session)
    # pathwayImportService.import_pathway()
    #
    # patientImportService = PatientImportService(primary_session, secondary_session)
    # patientImportService.import_patients_and_referrals()
