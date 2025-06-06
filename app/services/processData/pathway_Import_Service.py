from datetime import timedelta

from sqlalchemy import func, distinct, or_, and_, literal_column
from sqlalchemy.orm import Session

from app.models.admissions import ReferralStatusEnum
from app.models.pathway import PathwayStatusEnum, PathwayOutcomeEnum, PathwayProgress
from app.models.primary.Episode import Episode
from app.models.primary.Subject import Subject
from app.models.primary.Referrals import Referrals
from app.models.primary.Pathway import Pathway
from app.models.primary.PathwayForms import PathwayForms
from app.models.primary.AfFormData import AfFormData
from app.models.primary.Pathway import pathway_form_map

""" pathway details from primary database is ported to  pathway table of metrics database """
class PathwayImportService:
    def __init__(self, primary_db: Session, secondary_db: Session):
        self.primary_db = primary_db
        self.secondary_db = secondary_db

    def import_pathway(self):
        # If you want to use this as an entry point:
        self.import_pathway_progress()

    def import_pathway_progress(self):
        session = self.primary_db

        results = (
            session.query(
                Episode.episode_id.label("id"),
                Subject.subject_id.label("patient_id"),
                Episode.start_date.label("admission_time"),
                Episode.modified_date.label("modified_date"),
                Episode.status.label("episode_status"),
                Referrals.referral_status.label("referral_status"),
                func.count(distinct(pathway_form_map.c.formsSet_KEY)).label("steps_total"),
                func.count(distinct(AfFormData.afo_id)).label("steps_completed"),
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

        def map_status(episode_status, referral_status):
            if episode_status and episode_status.lower() == "discharged":
                return PathwayStatusEnum.COMPLETED
            elif episode_status and episode_status.lower() == "suspended":
                return PathwayStatusEnum.DROPPED
            elif episode_status and episode_status.lower() == "active":
                return PathwayStatusEnum.ACTIVE

            if referral_status is not None:
                if referral_status == ReferralStatusEnum.COMPLETED:
                    return PathwayStatusEnum.COMPLETED
                elif referral_status == ReferralStatusEnum.REFERRED_OUT:
                    return PathwayStatusEnum.DROPPED
                elif referral_status in (ReferralStatusEnum.PENDING, ReferralStatusEnum.REFERRED_IN):
                    return PathwayStatusEnum.ACTIVE

            return PathwayStatusEnum.ACTIVE

        progress_records = []
        for row in results:
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
                diagnosis_time=(row.admission_time + timedelta(minutes=row.diagnosis_minutes) if row.diagnosis_minutes and row.admission_time else None),
                had_complication=False,
                had_relapse=False
            )
            progress_records.append(progress)

        self.secondary_db.add_all(progress_records)
        self.secondary_db.commit()
