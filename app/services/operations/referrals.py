from datetime import date

from app.models.patient import Patient
from app.models.admissions import ReferralAdmission, ReferralStatusEnum

# Assuming you have the patient and clinician objects loaded
new_referral_in = ReferralAdmission(
    patient_id=Patient.id,
    referral_date=date.today(),
    referral_status=ReferralStatusEnum.REFERRED_IN,
    referral_type="In",
    clinician_id=clinician.id
)
session.add(new_referral_in)
session.commit()

new_referral_out = ReferralAdmission(
    patient_id=Patient.id,
    referral_date=date.today(),
    referral_status=ReferralStatusEnum.REFERRED_OUT,
    referral_type="Out",
    clinician_id=clinician.id
)
session.add(new_referral_out)
session.commit()

discharge_record = ReferralAdmission(
    patient_id=Patient.id,
    discharge_date=date.today(),
    referral_status=ReferralStatusEnum.DISCHARGED,
    referral_type="In",  # "In" because this patient was referred in
    clinician_id=clinician.id,
    discharge_notes="Patient has recovered and is discharged from the system."
)
session.add(discharge_record)
session.commit()
