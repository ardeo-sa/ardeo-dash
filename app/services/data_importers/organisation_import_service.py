"""
This module provides a service for importing organisation data from a primary database
into a metrics database.

The `OrganisationImportService` reads organisation records from the primary database,
maps them into the appropriate format, and writes them into the secondary (metrics) database.

This allows metrics-specific systems to maintain an up-to-date view of organisation data
without duplicating logic from the primary system.
"""
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.primary import Organisation as PrimaryOrganisation
from app.models.organisation import Organisation as MetricOrganisation
from app.models.primary.users import Users

logger = logging.getLogger(__name__)

class OrganisationImportService:
    """
    A service to import organisations from the primary database into the metrics database.

    This class reads data from the `PrimaryOrganisation` table and replicates it into
    the metrics-side `organisation` table.

    Attributes:
        primary_db (Session): SQLAlchemy session connected to the primary database.
        secondary_db (Session): SQLAlchemy session connected to the metrics database.
    """
    def __init__(self, primary_db: Session, secondary_db: Session):
        """
        Initialize the service with primary and secondary SQLAlchemy sessions.

        Args:
            primary_db (Session): SQLAlchemy session for reading from the source (primary) DB.
            secondary_db (Session): SQLAlchemy session for writing to the target (metrics) DB.
        """
        self.primary_db = primary_db
        self.secondary_db = secondary_db

    def import_organisation(self):
        """
        Fetches organisation records from the primary database and inserts them
        into the metrics database.

        This method creates `MetricOrganisation` instances from `PrimaryOrganisation`
        records and commits them in bulk to ensure consistency.
        """
        logger.info("Starting organisation import process.")

        try:
            organisations = self.primary_db.query(PrimaryOrganisation).outerjoin(Users.roles).all()
            logger.debug(f"Fetched {len(organisations)} organisations from primary DB.")
        except Exception as e:
            logger.exception("Failed to fetch organisations from primary DB. %s", e)
            raise

        organisationsmetric = {}

        for org in organisations:
            try:
                metricorg = MetricOrganisation(
                    id=org.id,
                    name=org.name,
                    code=org.code
                )
                organisationsmetric[org.id] = metricorg
                logger.debug(f"Prepared organisation: id={org.id}, name={org.name}")
            except SQLAlchemyError as e:
                logger.exception(f"Failed to process organisation: id={org.id} {e}")
                continue

        try:
            self.secondary_db.add_all(organisationsmetric.values())
            self.secondary_db.commit()
            logger.info(f"Successfully imported {len(organisationsmetric)} organisations.")
        except Exception as e:
            self.secondary_db.rollback()
            logger.exception("Failed to commit organisations to metrics DB. %s", e)
            raise
