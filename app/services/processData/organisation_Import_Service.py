from sqlalchemy.orm import Session
from app.models.primary import Organisation as PrimaryOrganisation
from app.models import Organisation as MetricOrganisation

""" organisations from primary database is copied to organisations table of metrics database """
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
        """Fetch organisations from primary DB and upsert into metrics DB."""
        organisations = self.primary_db.query(PrimaryOrganisation).all()

        for org in organisations:
            # Check if organisation already exists in secondary DB
            existing_org = self.secondary_db.query(MetricOrganisation).filter_by(id=org.id).first()

            if existing_org:
                # Update existing record
                existing_org.name = org.name
                existing_org.code = org.code
            else:
                # Create new record
                new_org = MetricOrganisation(
                    id=org.id,
                    name=org.name,
                    code=org.code
                )
                self.secondary_db.add(new_org)

        self.secondary_db.commit()











