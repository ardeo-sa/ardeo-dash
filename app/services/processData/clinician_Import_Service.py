from sqlalchemy.orm import Session
from app.models.clinician import Clinician
from app.models.primary.Users import Users

""" users from primary database is copied to clinician table of metrics database """
class ClinicianImportService:
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
        """Fetch username and roles from primary DB and upsert into metrics DB."""
        # Query all users with their roles
        users = self.primary_db.query(Users).outerjoin(Users.roles).all()

        for user in users:
            # Check if clinician already exists in secondary DB
            existing_clinician = self.secondary_db.query(Clinician).filter_by(id=user.user_id).first()

            # Collect role values as strings (deduplicated)
            role_values = [
                role.value
                for role in user.roles
                if role is not None
            ]
            role_values = list(set(role_values))

            if existing_clinician:
                # Update existing record
                existing_clinician.name = user.username
                existing_clinician.user_role = role_values
            else:
                # Create new record
                new_clinician = Clinician(
                    id=user.user_id,
                    name=user.username,
                    user_role=role_values
                )
                self.secondary_db.add(new_clinician)

        self.secondary_db.commit()