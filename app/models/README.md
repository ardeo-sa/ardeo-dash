## Model key points:

* ReferralStatusEnum: This enum is used to track the status of the referral/admission. It helps to distinguish between:
  * Referred In: A patient coming into the system. 
  * Referred Out: A patient being referred out to another facility. 
  * Discharged: A patient being discharged from the system. 
  * Pending: Referral is in progress. 
  * Completed: Referral has been completed (successful treatment, etc.). 
  * Cancelled: Referral has been cancelled. 
* referral_type: This distinguishes between "In" and "Out" referrals. For example:
  * Referral In could represent when a patient is referred from primary care to secondary care. 
  * Referral Out could represent when a patient is referred from secondary care to another hospital or back to the primary care physician. 
* Foreign Keys:
  * The patient_id column links this referral/admission record to a specific patient. 
  * The clinician_id links the referral/admission to the clinician responsible for it. 
  * The treatment_plan_id links to a treatment plan if a treatment has been assigned (this is optional and can be set to None if not applicable). 
* Discharge Date: The discharge_date field captures when the patient is discharged from the system, applicable to referrals and admissions that result in patient discharge. 

## Relationships:
  * Patient: A patient can have multiple referrals/admissions (one-to-many relationship). 
  * User (Clinician): A clinician can manage multiple referrals (one-to-many relationship). 
  * Treatment: A referral may be linked to a treatment plan that tracks what treatment the patient is receiving (optional).

## TODO - complete description of other models