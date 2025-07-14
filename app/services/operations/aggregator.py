from app.database.primary import PrimarySessionLocal
from app.services.operations.subject_Service import subject_Service
from app.services.operations.pathway_Service import pathway_Service

"""
   Processes and aggregates admission and treatment-related data from the primary database.

   This function initializes service classes for subjects and pathways,
   then collects various metrics including:
       - Daily, weekly, and monthly admissions and discharges
       - Average length of stay (ALOS)
       - Pathway adherence rate
       - Days to treatment 
       - using primary database
   """
def process_data():
    session = PrimarySessionLocal()

    subject_service = subject_Service(session)
    df_day = subject_service.admissions_discharges_by_day()
    df_week = subject_service.admissions_discharges_by_week()
    df_month = subject_service.admissions_discharges_by_month()
    df_alos = subject_service.average_length_of_stay()

    pathway_service = pathway_Service(session)
    adherence_rate=pathway_service.pathway_adherence_rate()
    days_to_treatment=pathway_service.days_to_treatment()