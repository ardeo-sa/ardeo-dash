"""
This module is responsible for creating and saving referral records for patients in the `ReferralAdmission` table.

The following records are created:
1. **Referral In**: A new referral is made for a patient being referred into the system by a clinician.
2. **Referral Out**: A new referral is made for a patient being referred out of the system.
3. **Discharge Record**: A record is created when a patient is discharged from the system, marking their recovery
and completion of care.

The module utilizes the `ReferralAdmission` model, patient data, and clinician information to log these events.
Each referral record is committed to the database to ensure persistent storage.
"""
from datetime import date

from app.models.admissions import ReferralAdmission, ReferralStatusEnum
from app.models.patient import Patient


def create_referral_in(patient: Patient, clinician_id: int, session) -> None:
    """
    Creates a new referral record for a patient being referred into the system.

    Args:
        patient (Patient): The ID of the patient being referred in.
        clinician_id (int): The ID of the clinician referring the patient in.
        session (Session): The SQLAlchemy session used for database operations.

    Returns:
        None
    """
    new_referral_in = ReferralAdmission(
        patient_id=patient.id,
        referral_date=date.today(),
        referral_status=ReferralStatusEnum.REFERRED_IN,
        referral_type="In",
        clinician_id=clinician_id
    )
    session.add(new_referral_in)
    session.commit()


def create_referral_out(patient: Patient, clinician_id: int, session) -> None:
    """
    Creates a new referral record for a patient being referred out of the system.

    Args:
        patient_id (int): The ID of the patient being referred out.
        clinician_id (int): The ID of the clinician referring the patient out.
        session (Session): The SQLAlchemy session used for database operations.

    Returns:
        None
    """
    new_referral_out = ReferralAdmission(
        patient_id=patient.id,
        referral_date=date.today(),
        referral_status=ReferralStatusEnum.REFERRED_OUT,
        referral_type="Out",
        clinician_id=clinician_id
    )
    session.add(new_referral_out)
    session.commit()


def create_discharge_record(patient: Patient, clinician_id: int, discharge_notes: str, session) -> None:
    """
    Creates a new discharge record for a patient who is being discharged from the system after recovery.

    Args:
        patient (Patient): The ID of the patient being discharged.
        clinician_id (int): The ID of the clinician handling the discharge.
        discharge_notes (str): A note indicating the reason for discharge or any additional relevant details.
        session (Session): The SQLAlchemy session used for database operations.

    Returns:
        None
    """
    discharge_record = ReferralAdmission(
        patient_id=patient.id,
        discharge_date=date.today(),
        referral_status=ReferralStatusEnum.DISCHARGED,
        referral_type="In",  # "In" because this patient was referred in
        clinician_id=clinician_id,
        discharge_notes=discharge_notes
    )
    session.add(discharge_record)
    session.commit()


def handle_referral_and_discharge(patient_id: int, clinician_id: int, discharge_notes: str, session) -> None:
    """
    Handles the creation of referral records and discharge records for a patient.

    This function will create a referral in record, referral out record, and discharge record as needed.

    Args:
        patient_id (int): The ID of the patient.
        clinician_id (int): The ID of the clinician.
        discharge_notes (str): A note indicating the reason for discharge.
        session (Session): The SQLAlchemy session used for database operations.

    Returns:
        None
    """
    patient = session.query(Patient).filter(Patient.id == patient_id).one_or_none()
    if not patient:
        raise ValueError(f"Patient with id {patient_id} not found")

    create_referral_in(patient, clinician_id, session)
    create_referral_out(patient, clinician_id, session)
    create_discharge_record(patient, clinician_id, discharge_notes, session)
