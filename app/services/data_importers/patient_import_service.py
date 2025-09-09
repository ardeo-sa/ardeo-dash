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
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.reporting.admissions import ReferralAdmission, ReferralStatusEnum
from app.models.reporting.patient import Patient
from app.models.primary.episode import Episode
# from app.models.primary.subject import Subject
from app.models.primary.referrals import Referrals

logger = logging.getLogger(__name__)
# pylint: disable=too-many-statements

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
            logger.debug(f"Fetched {len(referrals_with_episodes)} referrals with associated episodes from primary DB.")
        except Exception as e:
            logger.exception("Failed to fetch referrals and episodes. %s", e)
            raise

        referral_status_enum = {
            0: ReferralStatusEnum.PENDING,
            1: ReferralStatusEnum.REFERRED_IN,
            2: ReferralStatusEnum.REFERRED_OUT,
            3: ReferralStatusEnum.COMPLETED,
            4: ReferralStatusEnum.REFERRED_IN,
        }

        inserted_patients = 0
        updated_patients = 0
        inserted_referrals = 0
        updated_referrals = 0

        # --- Process each referral ---
        for i, ref in enumerate(referrals_with_episodes, start=1):
            try:
                ep = ref.episode
                subj = ep.subject

                # --- UPSERT PATIENT ---
                existing_patient = (
                    self.secondary_db.query(Patient)
                    .filter_by(primary_guid=subj.guid)
                    .first()
                )

                if existing_patient:
                    existing_patient.name = subj.fullname
                    existing_patient.admission_date = ep.start_date
                    existing_patient.discharge_date = ep.modified_date
                    existing_patient.status = ep.status
                    patient = existing_patient
                    updated_patients += 1
                    logger.debug(f"[{i}] Updated patient {subj.guid} with episode_id={ep.episode_id}")
                else:
                    patient = Patient(
                        primary_guid=subj.guid,
                        name=subj.fullname,
                        admission_date=ep.start_date,
                        discharge_date=ep.modified_date,
                        status=ep.status,
                    )
                    self.secondary_db.add(patient)
                    self.secondary_db.flush()  # assign patient.id
                    inserted_patients += 1
                    logger.debug(f"[{i}] Inserted patient {subj.guid} with episode_id={ep.episode_id}")

                # --- UPSERT REFERRAL ---
                status_enum = referral_status_enum.get(ref.referral_status, ReferralStatusEnum.PENDING)

                existing_referral = (
                    self.secondary_db.query(ReferralAdmission)
                    .filter_by(
                        patient_id=patient.id,
                        referral_date=ref.referral_date,
                        pathway_id=ref.pathway_id,
                    )
                    .first()
                )

                if existing_referral:
                    existing_referral.admit_time = ep.start_date
                    existing_referral.discharge_time = ep.modified_date
                    existing_referral.referral_status = status_enum
                    existing_referral.referral_type = "In"
                    existing_referral.referring_clinician_id = ref.referred_from_user_id
                    existing_referral.receiving_clinician_id = ref.referred_to_user_id
                    existing_referral.receiving_organisation_id = ref.referring_to_organisation
                    existing_referral.discharge_notes = ""
                    updated_referrals += 1
                    logger.debug(f"[{i}] Updated referral for patient_id={patient.id}")
                else:
                    new_referral = ReferralAdmission(
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
                        discharge_notes="",
                    )
                    self.secondary_db.add(new_referral)
                    inserted_referrals += 1
                    logger.debug(f"[{i}] Inserted referral for patient_id={patient.id}")

            except (AttributeError, TypeError, IntegrityError, SQLAlchemyError) as e:
                logger.exception(
                    "[%d] Failed to process referral id=%s: %s", i, getattr(ref, "id", "N/A"), e
                )
                continue

        # --- Commit ---
        try:
            self.secondary_db.commit()
            logger.info(
                f"Referral import complete: "
                f"{inserted_patients} inserted, {updated_patients} updated patients; "
                f"{inserted_referrals} inserted, {updated_referrals} updated referrals."
            )
        except Exception as e:
            self.secondary_db.rollback()
            logger.exception("Failed to commit referral import to secondary DB. %s", e)
            raise
