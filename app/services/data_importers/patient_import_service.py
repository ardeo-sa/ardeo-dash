"""
This module defines the PatientImportService class used to import patient and referral data
from a primary database into a metrics database.

It retrieves subjects, episodes, and referrals from the primary database, creates corresponding
Patient and ReferralAdmission records, and stores them in the metrics (secondary) database.

Assumptions:
- Referral status codes are mapped to ReferralStatusEnum.
- Discharge notes are not yet available and require additional data sources.
"""
import logging

from sqlalchemy.orm import Session, joinedload

from app.models.admissions import ReferralAdmission, ReferralStatusEnum
from app.models.patient import Patient
from app.models.primary.episode import Episode
# from app.models.primary.subject import Subject
from app.models.primary.referrals import Referrals

logger = logging.getLogger(__name__)


class PatientImportService:
    """
        Service class for importing patient and referral information from a primary
        clinical database to a metrics database.

        Attributes:
            primary_db (Session): SQLAlchemy session connected to the primary database.
            secondary_db (Session): SQLAlchemy session connected to the secondary/metrics database.
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

    def import_patients_and_referrals(self):
        """
            Imports patients and their associated referrals from the primary database
            into the metrics database.

            - Joins referrals with their associated episodes and subjects.
            - Creates a Patient record in the metrics DB for each subject.
            - Creates a ReferralAdmission record for each referral.
            - Maps integer referral statuses to ReferralStatusEnum values.
            - Discharge notes are left blank and can be populated later from comments.

            Commits all data in a single batch at the end for performance.
        """
        logger.info("Starting import of patients and referrals.")

        try:
            referrals_with_episodes = (
                self.primary_db.query(Referrals)
                .join(Referrals.episode)
                .join(Episode.subject)
                .options(
                    joinedload(Referrals.episode).joinedload(Episode.subject)
                )
                .all()
            )
            logger.info(f"Fetched {len(referrals_with_episodes)} referrals with associated episodes.")
        except Exception:
            logger.exception("Failed to fetch referrals and episodes.")
            raise

        referral_status_enum = {
            0: ReferralStatusEnum.PENDING,
            1: ReferralStatusEnum.REFERRED_IN,
            2: ReferralStatusEnum.REFERRED_OUT,
            3: ReferralStatusEnum.COMPLETED,
            4: ReferralStatusEnum.REFERRED_IN,
        }

        imported_patients = 0
        imported_referrals = 0

        for i, ref in enumerate(referrals_with_episodes, start=1):
            try:
                ep=ref.episode
                subj =ep.subject

                # Create Patient
                patient = Patient(
                    primary_guid=subj.guid,
                    name=subj.fullname,
                    admission_date=ep.start_date,
                    discharge_date=ep.modified_date,
                    status=ep.status
                )

                self.secondary_db.add(patient)
                self.secondary_db.flush()
                imported_patients += 1
                logger.debug(f"[{i}] Added patient {subj.guid} with episode_id {ep.episode_id}.")

                # Create ReferralAdmissions (if any)
                status_enum = referral_status_enum.get(ref.referral_status, ReferralStatusEnum.PENDING)

                referral = ReferralAdmission(
                    admit_time=ep.start_date,
                    discharge_time=ep.modified_date,
                    patient_id=patient.id,
                    referral_date=ref.referral_date,
                    referral_status=status_enum,
                    referral_type="In",
                    referring_clinician_id=ref.referred_from_user_id,
                    receiving_clinician_id=ref.referred_to_user_id,
                    receiving_organisation_id=ref.referring_to_organisation,
                    pathway_id=ref.pathway_id,
                    discharge_notes= ""
                    # """ discharge_notes not updated yet can be derived from comments table not ported to primary db """
                )

                self.secondary_db.add(referral)
                imported_referrals += 1
                logger.debug(f"[{i}] Added referral for patient {patient.id}.")
            except Exception:
                logger.exception(f"[{i}] Failed to process referral with id={ref.id if ref else 'N/A'}.")

        try:
            self.secondary_db.commit()
            logger.info(
                f"Import complete: {imported_patients} patients and {imported_referrals} referrals committed.")
        except Exception:
            self.secondary_db.rollback()
            logger.exception("Failed to commit data to secondary database.")
            raise