"""
This module defines the ClinicianImportService class, which handles importing user data
from the primary database into the clinician table of the metrics database.

It reads Users and their associated roles from the primary database, transforms the data
by consolidating user roles, and stores the resulting Clinician records into the secondary
(metrics) database.

This facilitates synchronizing clinician information between the primary user system and the metrics reporting system.
"""
from sqlalchemy.orm import Session

from app.models.clinician import Clinician
from app.models.primary.users import Users

class ClinicianImportService:
    """
    Service to import and synchronize clinician data from the primary user database
    to the metrics database.

    It extracts user information and roles from the primary database, consolidates
    role data, and inserts or updates corresponding Clinician records in the
    secondary metrics database.
    """
    def __init__(self, primary_db: Session, secondary_db: Session):
        """
        Initialize the service with primary and secondary SQLAlchemy sessions.

        Args:
            primary_db (Session): SQLAlchemy session for reading from the source (primary) DB.
            secondary_db (Session): SQLAlchemy session for writing to the target (secondary) DB.
        """
        self.primary_db = primary_db
        self.secondary_db = secondary_db

    def import_clinician(self):
        """ username and roles(as concatenated string)  are fetched and stored from primary db to metrics db """
        # Query all users with their roles (ORM style)
        users = self.primary_db.query(Users).outerjoin(Users.roles).all()

        clinicians = {}

        for user in users:
            clinician = Clinician(
                id=user.user_id,
                name=user.username
            )

            # Collect role values as strings
            role_values = [
                role.value
                for role in user.roles
                if role is not None
            ]
            clinician.user_role = list(set(role_values))  # Deduplicate roles

            clinicians[user.user_id] = clinician

        self.secondary_db.add_all(clinicians.values())
        self.secondary_db.commit()
