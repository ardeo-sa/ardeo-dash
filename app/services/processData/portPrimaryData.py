from app.database.metrics import MetricsSessionLocal
from app.database.primary import PrimarySessionLocal
from app.services.processData.clinician_Import_Service import ClinicianImportService
from app.services.processData.mdt_Import_Service import MdtImportService
from app.services.processData.organisation_Import_Service import OrganisationImportService
from app.services.processData.pathway_Import_Service import PathwayImportService
from app.services.processData.patient_Import_Service import PatientImportService

"""
Migrates data from the primary database to the metrics database.

This function handles the end-to-end process of fetching relevant data
from the primary database and inserting or updating it into the metrics
database to ensure synchronized reporting and analytics.
"""

def portprimarydata():
    primary_session = PrimarySessionLocal()
    secondary_session = MetricsSessionLocal()

    clinicianImportService = ClinicianImportService(primary_session,secondary_session)
    clinicianImportService.import_clinician()

    organisationsImportService = OrganisationImportService(primary_session, secondary_session)
    organisationsImportService.import_organisation()


    mdtImportService = MdtImportService(primary_session,secondary_session)
    mdtImportService.import_mdt()


    pathwayImportService = PathwayImportService(primary_session, secondary_session)
    pathwayImportService.import_pathway()

    patientImportService = PatientImportService(primary_session, secondary_session)
    patientImportService.import_patients_and_referrals()