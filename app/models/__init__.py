"""
This package initializes and aggregates core healthcare models used throughout the system.

It provides centralized imports for key domain entities such as referrals, appointments,
clinicians, MDT meetings, messaging, metrics, patient pathways, and treatments.

These models represent the fundamental components of clinical workflows, operational analytics,
and administrative tracking within the healthcare platform.

Modules Included:
- Admissions and Referrals (ReferralAdmission, ReferralStatusEnum, Referral)
- Appointments (Appointment)
- Clinicians and Tasks (Clinician, ClinicianTask)
- MDT (MDTMeeting, MDTCase, MDTAction, MDTParticipant)
- Messaging (Message, Conversation)
- Metrics (PatientMetrics, OperationalMetrics, MDTMetrics, AdminMetrics, ClinicianMetrics,
  PathwayMetrics, ReferralMetrics)
- Organisation and Patient (Organisation, Patient)
- Pathways (PathwayProgress)
- Treatments (Treatment, TreatmentSlotBooking)
"""

from app.models.reporting.admissions import ReferralAdmission
from app.models.reporting.admissions import ReferralStatusEnum
from app.models.reporting.appointments import Appointment
from app.models.reporting.clinician import Clinician
from app.models.reporting.clinician import ClinicianTask
from app.models.reporting.mdt import MDTAction
from app.models.reporting.mdt import MDTMeeting
from app.models.reporting.mdt import MDTCase
from app.models.reporting.mdt import MDTParticipant

from app.models.reporting.messaging import Message
from app.models.reporting.messaging import Conversation
from app.models.reporting.metrics import PatientMetrics
from app.models.reporting.metrics import OperationalMetrics
from app.models.reporting.metrics import MDTMetrics
from app.models.reporting.metrics import AdminMetrics
from app.models.reporting.metrics import ClinicianMetrics
from app.models.reporting.metrics import PathwayMetrics
from app.models.reporting.metrics import ReferralMetrics
from app.models.reporting.organisation import Organisation
from app.models.reporting.pathway import PathwayProgress
from app.models.reporting.patient import Patient
from app.models.reporting.referrals import Referral
from app.models.reporting.treatments import Treatment
from app.models.reporting.treatments import TreatmentSlotBooking
