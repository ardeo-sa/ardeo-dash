"""
This module defines the `PathwayImportService` which is responsible for importing and transforming
pathway progress data from a primary database into the metrics system.

It pulls data from multiple models in the primary database including `Episode`, `Subject`,
`Referrals`, `PathwayForms`, and `AfFormData`, performs aggregation and transformation, and
writes results into the `PathwayProgress` model in the secondary database.
"""
import logging
from datetime import timedelta

from sqlalchemy import func, distinct, or_, and_, literal_column
from sqlalchemy.orm import Session

from app.models.admissions import ReferralStatusEnum
from app.models.pathway import PathwayStatusEnum, PathwayOutcomeEnum, PathwayProgress
from app.models.primary.episode import Episode
from app.models.primary.subject import Subject
from app.models.primary.referrals import Referrals
from app.models.primary.pathway import Pathway
from app.models.primary.pathway_forms import PathwayForms
from app.models.primary.af_form_data import AfFormData
from app.models.primary.pathway import pathway_form_map

logger = logging.getLogger(__name__)


class PathwayImportService:
    """
       Service class responsible for importing patient pathway progress data from the primary database
       into the metrics system.

       Attributes:
           primary_db (Session): SQLAlchemy session for reading from the primary/source database.
           secondary_db (Session): SQLAlchemy session for writing to the secondary/target database.
    """
    def __init__(self, primary_db: Session, secondary_db: Session):
        """
           Initialize the import service with primary and secondary database sessions.

           Args:
               primary_db (Session): SQLAlchemy session for reading from the source database.
               secondary_db (Session): SQLAlchemy session for writing to the metrics database.
        """
        self.primary_db = primary_db
        self.secondary_db = secondary_db

    def import_pathway(self):
        """
            Entry point method to trigger pathway data import.

            Currently delegates to `import_pathway_progress` to perform the import logic.
        """
        logger.info("Starting pathway import process.")
        self.import_pathway_progress()

    def import_pathway_progress(self):
        """
           Imports pathway progress data by aggregating episode, referral, and form completion information.

           It joins several primary database tables to compute:
           - Total and completed pathway steps
           - Admission, treatment, and diagnosis times
           - Status based on episode or referral status

           The processed data is then written to the `PathwayProgress` table in the secondary database.
        """
        logger.info("Querying pathway progress data from primary DB.")
        session = self.primary_db

        try:
            results = (
                session.query(
                    Episode.episode_id.label("id"),
                    Subject.subject_id.label("patient_id"),
                    Episode.start_date.label("admission_time"),
                    Episode.modified_date.label("modified_date"),
                    Episode.status.label("episode_status"),
                    Referrals.referral_status.label("referral_status"),
                    func.count(distinct(pathway_form_map.c.formsSet_KEY)).\
                    label("steps_total"), # pylint: disable=not-callable
                    func.count(distinct(AfFormData.afo_id)).label("steps_completed"),# pylint: disable=not-callable
                    func.min(AfFormData.creation_date).label("treatment_start_time"),
                    func.max(AfFormData.creation_date).label("treatment_end_time"),
                    func.timestampdiff(
                        literal_column("MINUTE"),
                        Episode.start_date,
                        Episode.modified_date
                    ).label("diagnosis_minutes")
                )
                .join(Subject, Subject.subject_id == Episode.subject_id)
                .join(Referrals, Referrals.episode_id == Episode.episode_id)
                .outerjoin(Pathway, or_(
                    Pathway.id == Episode.pathway_id,
                    Pathway.id == Referrals.pathway_id
                ))
                .join(pathway_form_map, pathway_form_map.c.pathway_id.in_([
                    Episode.pathway_id, Referrals.pathway_id
                ]))
                .join(PathwayForms, PathwayForms.pathway_form_id == pathway_form_map.c.formsSet_KEY)
                .outerjoin(AfFormData, and_(
                    AfFormData.episode_id == Episode.episode_id,
                    AfFormData.afo_id == PathwayForms.afobject_id
                ))
                .group_by(
                    Episode.episode_id, Subject.subject_id,
                    Episode.start_date, Episode.modified_date,
                    Episode.status, Referrals.referral_status
                )
                .all()
            )
            logger.info(f"Fetched {len(results)} pathway records.")
        except Exception as e:
            logger.exception("Failed to query pathway data. %s", e)
            raise

        def map_status(episode_status, referral_status):
            """
                Maps episode and referral status values to a unified `PathwayStatusEnum` value.

                Args:
                    episode_status (str): The status of the episode (e.g., "active", "discharged").
                    referral_status (ReferralStatusEnum): Enum value representing the referral status.

                Returns:
                    PathwayStatusEnum: The mapped pathway status.
            """
            if episode_status:
                status_lower = episode_status.lower()
                if status_lower == "discharged":
                    return PathwayStatusEnum.COMPLETED
                if status_lower == "suspended":
                    return PathwayStatusEnum.DROPPED
                if status_lower == "active":
                    return PathwayStatusEnum.ACTIVE

            if referral_status in {
                ReferralStatusEnum.COMPLETED,
                ReferralStatusEnum.REFERRED_OUT,
                ReferralStatusEnum.PENDING,
                ReferralStatusEnum.REFERRED_IN,
            }:
                return {
                    ReferralStatusEnum.COMPLETED: PathwayStatusEnum.COMPLETED,
                    ReferralStatusEnum.REFERRED_OUT: PathwayStatusEnum.DROPPED,
                    ReferralStatusEnum.PENDING: PathwayStatusEnum.ACTIVE,
                    ReferralStatusEnum.REFERRED_IN: PathwayStatusEnum.ACTIVE,
                }[referral_status]

            return PathwayStatusEnum.ACTIVE

        progress_records = []
        for i, row in enumerate(results, start=1):
            try:
                status = map_status(row.episode_status, row.referral_status)
                progress = PathwayProgress(
                    id=row.id,
                    patient_id=row.patient_id,
                    steps_total=row.steps_total or 0,
                    steps_completed=row.steps_completed or 0,
                    status=status,
                    outcome=PathwayOutcomeEnum.UNKNOWN,
                    readmitted=False,
                    admission_time=row.admission_time,
                    treatment_start_time=row.treatment_start_time,
                    treatment_end_time=row.treatment_end_time,
                    diagnosis_time=(row.admission_time + timedelta(minutes=row.diagnosis_minutes)
                                    if row.diagnosis_minutes and row.admission_time else None),
                    had_complication=False,
                    had_relapse=False
                )
                progress_records.append(progress)
                logger.debug(f"[{i}] Mapped progress for episode_id={row.id}")
            except (AttributeError, TypeError) as e:
                logger.exception(f"Failed to map pathway progress for episode_id={row.id} {e}", e)

        try:
            self.secondary_db.add_all(progress_records)
            self.secondary_db.commit()
            logger.info(f"Successfully committed {len(progress_records)} pathway progress records.")
        except Exception as e:
            self.secondary_db.rollback()
            logger.exception("Failed to commit pathway progress records to secondary DB. %s", e)
            raise
