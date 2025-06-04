from sqlalchemy.orm import Session, contains_eager, joinedload
from app.models.clinician import Clinician
from app.models.primary import Organisation as PrimaryOrganisation
from app.models import Organisation as MetricOrganisation
from app.models.primary.Users import Users

class OrganisationImportService:
    def __init__(self, primary_db: Session, secondary_db: Session):
        """
        Initialize the service with primary and secondary SQLAlchemy sessions.

        Args:
            primary_db (Session): SQLAlchemy session for reading from the source (primary) DB.
            secondary_db (Session): SQLAlchemy session for writing to the target (secondary) DB.
        """
        self.primary_db = primary_db
        self.secondary_db = secondary_db

    def import_organisation(self):
        # Query all users with their roles (ORM style)
        organisations = self.primary_db.query(PrimaryOrganisation).outerjoin(Users.roles).all()

        organisationsmetric = {}

        for org in organisations:
            metricorg = MetricOrganisation(
                id=org.id,
                name = org.name,
                code = org.code
            )
            organisationsmetric[org.id] = metricorg

        self.secondary_db.add_all(organisationsmetric.values())
        self.secondary_db.commit()











