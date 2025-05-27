from sqlalchemy.orm import Session, contains_eager, joinedload
from app.models.clinician import Clinician
from app.models.primary.Users import Users


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
        # Query all users with their roles (ORM style)
        users = self.primary_db.query(Users).outerjoin(Users.roles).all()

        clinicians = {}

        for user in users:
            clinician = Clinician(
                id=user.user_id,
                name=user.user_username
            )

            # Collect role values as strings
            role_values = [
                ur.role.value
                for ur in user.roles
                if ur.role is not None
            ]
            clinician.user_role = list(set(role_values))  # Deduplicate roles

            clinicians[user.user_id] = clinician

        self.secondary_db.add_all(clinicians.values())
        self.secondary_db.commit()











