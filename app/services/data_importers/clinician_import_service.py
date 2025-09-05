"""
This module defines the ClinicianImportService class, which handles importing user data
from the primary database into the clinician table of the metrics database.

It reads Users and their associated roles from the primary database, transforms the data
by consolidating user roles, and stores the resulting Clinician records into the secondary
(metrics) database.

This facilitates synchronizing clinician information between the primary user system and the metrics reporting system.
"""
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.reporting.clinician import Clinician
from app.models.primary.users import Users

logger = logging.getLogger(__name__)


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
        logger.info("Starting clinician import process.")

        # Query all users with their roles
        try:
            users = self.primary_db.query(Users).outerjoin(Users.roles).all()
            logger.debug(f"Fetched {len(users)} users from primary DB.")
        except Exception as e:
            logger.exception("Failed to fetch users from primary DB. %s", e)
            raise

        processed_count = 0

        for user in users:
            try:
                # Check if clinician already exists in secondary DB
                existing_clinician = (
                    self.secondary_db.query(Clinician)
                    .filter_by(id=user.user_id)
                    .first()
                )

                # Collect role values as strings (deduplicated)
                role_values = list({role.value for role in user.roles if role is not None})

                if existing_clinician:
                    # Update existing record
                    existing_clinician.name = user.username
                    existing_clinician.user_role = role_values
                    logger.debug(f"Updated Clinician: id={user.user_id}, name={user.username}, roles={role_values}")
                else:
                    # Create new record
                    new_clinician = Clinician(
                        id=user.user_id,
                        name=user.username,
                        user_role=role_values,
                    )
                    self.secondary_db.add(new_clinician)
                    logger.debug(f"Inserted Clinician: id={user.user_id}, name={user.username}, roles={role_values}")

                processed_count += 1


            except SQLAlchemyError as e:
                logger.exception("Error processing user id=%s. %s", user.user_id, e)
                continue  # skip to next user instead of failing whole batch

        try:
            self.secondary_db.commit()
            logger.info(f"Successfully imported/updated {processed_count} clinicians into secondary DB.")
        except Exception as e:
            logger.exception("Failed to commit clinicians to secondary DB. %s", e)
            self.secondary_db.rollback()
            raise
