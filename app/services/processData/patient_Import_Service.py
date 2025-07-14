from sqlalchemy.orm import Session, contains_eager, joinedload

from app.models.admissions import ReferralAdmission, ReferralStatusEnum
from app.models.patient import Patient
from app.models.primary.episode import Episode
from app.models.primary.Subject import Subject
from app.models.primary.Referrals import Referrals

""" pathient details, treatement used and referrals  from primary database is ported to  patient and referral_admissions table of metrics database """
class PatientImportService:
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
        referrals_with_episodes = (
            self.primary_db.query(Referrals)
            .join(Referrals.episode)
            .join(Episode.subject)
            .options(
                joinedload(Referrals.episode).joinedload(Episode.subject)
            )
            .all()
        )
        for ref in referrals_with_episodes:
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

            # Create ReferralAdmissions (if any)

            referral_status_enum = {
                0: ReferralStatusEnum.PENDING,
                1: ReferralStatusEnum.REFERRED_IN,
                2: ReferralStatusEnum.REFERRED_OUT,  # or another value depending on use case
                3: ReferralStatusEnum.COMPLETED,
                4: ReferralStatusEnum.REFERRED_IN,  # OR create a new status like ADDED_TO_MEETING if needed
            }
            status_enum = referral_status_enum.get(ref.referral_status, ReferralStatusEnum.PENDING)

            referral = ReferralAdmission(
                admit_time=ep.start_date,
                discharge_time=ep.modified_date,
                patient_id=patient.id,
                referral_date=ref.referral_date,
                referral_status=status_enum,
                referral_type="In",  # or determine logic if needed
                referring_clinician_id=ref.referred_from_user_id,
                receiving_clinician_id=ref.referred_to_user_id,
                receiving_organisation_id=ref.referring_to_organisation,
                pathway_id=ref.pathway_id,
                discharge_notes= ""
                # """ discharge_notes not updated yet can be derived from comments table not ported to primary db """
            )
            self.secondary_db.add(referral)
            # Final commit to secondary DB
        self.secondary_db.commit()
