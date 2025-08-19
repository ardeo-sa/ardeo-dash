from sqlalchemy.orm import Session, joinedload

from app.models.admissions import ReferralAdmission, ReferralStatusEnum
from app.models.patient import Patient
from app.models.primary.Episode import Episode

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

        referral_status_enum = {
            0: ReferralStatusEnum.PENDING,
            1: ReferralStatusEnum.REFERRED_IN,
            2: ReferralStatusEnum.REFERRED_OUT,
            3: ReferralStatusEnum.COMPLETED,
            4: ReferralStatusEnum.REFERRED_IN,
        }

        for ref in referrals_with_episodes:
            ep = ref.episode
            subj = ep.subject

            # --- UPSERT PATIENT ---
            existing_patient = self.secondary_db.query(Patient).filter_by(primary_guid=subj.guid).first()
            if existing_patient:
                existing_patient.name = subj.fullname
                existing_patient.admission_date = ep.start_date
                existing_patient.discharge_date = ep.modified_date
                existing_patient.status = ep.status
                patient = existing_patient
            else:
                patient = Patient(
                    primary_guid=subj.guid,
                    name=subj.fullname,
                    admission_date=ep.start_date,
                    discharge_date=ep.modified_date,
                    status=ep.status
                )
                self.secondary_db.add(patient)
                self.secondary_db.flush()  # get patient.id for referral

            # --- UPSERT REFERRAL ---
            status_enum = referral_status_enum.get(ref.referral_status, ReferralStatusEnum.PENDING)

            existing_referral = self.secondary_db.query(ReferralAdmission).filter_by(
                patient_id=patient.id,
                referral_date=ref.referral_date,
                pathway_id=ref.pathway_id
            ).first()

            if existing_referral:
                existing_referral.admit_time = ep.start_date
                existing_referral.discharge_time = ep.modified_date
                existing_referral.referral_status = status_enum
                existing_referral.referral_type = "In"
                existing_referral.referring_clinician_id = ref.referred_from_user_id
                existing_referral.receiving_clinician_id = ref.referred_to_user_id
                existing_referral.receiving_organisation_id = ref.referring_to_organisation
                existing_referral.discharge_notes = ""
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
                    discharge_notes=""
                )
                self.secondary_db.add(new_referral)

        self.secondary_db.commit()

