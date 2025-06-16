from datetime import datetime, date
from uuid import uuid4

import pytest

from app.models.admissions import ReferralAdmission, ReferralStatusEnum
from app.models.appointments import Appointment
from app.models.clinician import Clinician,ClinicianTask
from app.models.mdt import MDTMeeting,MDTParticipant,MDTAction,MDTCase
from app.models.messaging import Message,Conversation
from app.models.metrics import MDTMetrics,ReferralMetrics,AdminMetrics,OperationalMetrics,PatientMetrics,PathwayMetrics,ClinicianMetrics
from app.models.Organisation import Organisation
from app.models.pathway import PathwayProgress, PathwayOutcomeEnum, PathwayStatusEnum
from app.models.patient import Patient
from app.models.referrals import Referral
from app.models.treatments import Treatment,TreatmentSlotBooking
from sqlalchemy.exc import IntegrityError

# testing admissions.py
def test_enum_values():
    assert ReferralStatusEnum.PENDING.value == "Pending"
    assert ReferralStatusEnum.REFERRED_IN.value == "Referred In"
    assert ReferralStatusEnum.REFERRED_OUT.value == "Referred Out"
    assert ReferralStatusEnum.DISCHARGED.value == "Discharged"
    assert ReferralStatusEnum.COMPLETED.value == "Completed"
    assert ReferralStatusEnum.CANCELLED.value == "Cancelled"


def test_create_referral_admission(db_session):
    # Create dummy related objects
    patient = Patient(
        primary_guid="abc-123-xyz",
        name="John Doe",
        admission_date=date(2024, 6, 1),
        discharge_date=date(2024, 6, 10),
        status="discharged"
    )
    referring_clinician = Clinician(name="Dr. Referrer")
    receiving_clinician = Clinician(name="Dr. Receiver")
    organisation = Organisation(name="Test Org", code="TEST001")

    db_session.add_all([patient, referring_clinician, receiving_clinician, organisation])
    db_session.commit()  # Commit first to get IDs

    # Now patient.id is available
    pathway = PathwayProgress(
        patient_id=patient.id,
        status=PathwayStatusEnum.ACTIVE,
        outcome=PathwayOutcomeEnum.SUCCESS,
        steps_total=5,
        steps_completed=5,
        readmitted=False,
        had_complication=False,
        had_relapse=False
    )

    db_session.add(pathway)
    db_session.commit()  # Commit to get pathway.id

    referral = ReferralAdmission(
        admit_time=datetime(2024, 1, 1, 10, 0),
        discharge_time=datetime(2024, 1, 5, 15, 0),
        patient_id=patient.id,
        referral_date=date(2024, 1, 1),
        discharge_date=date(2024, 1, 5),
        referral_type="In",
        referring_clinician_id=referring_clinician.id,
        receiving_clinician_id=receiving_clinician.id,
        receiving_organisation_id=organisation.id,
        pathway_id=pathway.id,
        discharge_notes="Patient recovered well."
    )

    db_session.add(referral)
    db_session.commit()

    fetched = db_session.query(ReferralAdmission).first()
    assert fetched is not None
    assert fetched.patient_id == patient.id
    assert fetched.referral_type == "In"
    assert fetched.referral_status == ReferralStatusEnum.PENDING  # default
    assert fetched.receiving_clinician.name == "Dr. Receiver"
    assert fetched.referring_clinician.name == "Dr. Referrer"
    assert fetched.organisation.name == "Test Org"


def test_referral_admission_missing_required_fields(db_session):
    with pytest.raises(IntegrityError):
        referral = ReferralAdmission(
            referral_type="Out",  # Missing patient_id and referring_clinician_id
        )
        db_session.add(referral)
        db_session.commit()

# testing appointments.py
def test_create_appointment(db_session):
    patient = Patient(
        primary_guid="abc-123-xyz",
        name="Test Patient",
        admission_date=date(2024, 6, 1),
        discharge_date=date(2024, 6, 10),
        status="discharged"
    )
    db_session.add(patient)
    db_session.commit()

    appointment = Appointment(
        patient_id=patient.id,
        scheduled_time=datetime(2024, 6, 16, 10, 0),
        attended=False,
        cancelled=False
    )
    db_session.add(appointment)
    db_session.commit()

    result = db_session.query(Appointment).first()
    assert result is not None
    assert result.patient_id == patient.id
    assert result.attended is False
    assert result.cancelled is False
    assert result.patient.name == "Test Patient"

# testing clinician.py
def test_create_clinician(db_session):
    clinician = Clinician(name="Dr. Smith", user_role="Consultant")
    db_session.add(clinician)
    db_session.commit()

    result = db_session.query(Clinician).first()
    assert result is not None
    assert result.name == "Dr. Smith"
    assert result.user_role == "Consultant"


def test_create_clinician_task(db_session):
    clinician = Clinician(name="Dr. House", user_role="Surgeon")
    db_session.add(clinician)
    db_session.commit()

    task = ClinicianTask(clinician_id=clinician.id, description="Review lab results")
    db_session.add(task)
    db_session.commit()

    result = db_session.query(ClinicianTask).first()
    assert result is not None
    assert result.description == "Review lab results"
    assert result.completed is False
    assert result.clinician.name == "Dr. House"


def test_clinician_task_requires_clinician(db_session):
    task = ClinicianTask(description="Orphan task")
    db_session.add(task)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_create_mdt_meeting(db_session):
    meeting = MDTMeeting(
        primary_guid="GUID-1234",
        meeting_time=datetime(2024, 6, 1, 10, 0),
        referral_time=datetime(2024, 5, 25, 14, 0),
        review_time=datetime(2024, 5, 30, 9, 30),
        meeting_start_time=datetime(2024, 6, 1, 10, 0),
        meeting_end_time=datetime(2024, 6, 1, 11, 0)
    )
    db_session.add(meeting)
    db_session.commit()

    assert meeting.id is not None
    assert meeting.primary_guid == "GUID-1234"


def test_add_participant_to_meeting(db_session):
    clinician = Clinician(name="Dr. MDT", user_role="Specialist")
    meeting = MDTMeeting(primary_guid="GUID-456")
    db_session.add_all([clinician, meeting])
    db_session.commit()

    participant = MDTParticipant(clinician_id=clinician.id, meeting_id=meeting.id)
    db_session.add(participant)
    db_session.commit()

    assert participant.id is not None
    assert participant.meeting.id == meeting.id
    assert participant.clinician.name == "Dr. MDT"

# testing mdt.py
def test_add_action_to_meeting(db_session):
    meeting = MDTMeeting(primary_guid="GUID-ACT")
    db_session.add(meeting)
    db_session.commit()

    action = MDTAction(meeting_id=meeting.id, completed=True)
    db_session.add(action)
    db_session.commit()

    assert action.id is not None
    assert action.completed is True
    assert action.meeting.id == meeting.id


def test_add_case_to_meeting(db_session):
    meeting = MDTMeeting(primary_guid="GUID-CASE")
    db_session.add(meeting)
    db_session.commit()

    case = MDTCase(meeting_id=meeting.id, patient_id=1001, discussion_notes="Patient requires review.")
    db_session.add(case)
    db_session.commit()

    assert case.id is not None
    assert case.patient_id == 1001
    assert case.meeting.id == meeting.id

# testing messaging.py
def test_create_conversation(db_session):
    conversation = Conversation(
        user1_id=uuid4(),
        user2_id=uuid4()
    )
    db_session.add(conversation)
    db_session.commit()

    assert conversation.id is not None
    assert conversation.created_at is not None


def test_create_message_in_conversation(db_session):
    user1 = uuid4()
    user2 = uuid4()
    conversation = Conversation(user1_id=user1, user2_id=user2)
    db_session.add(conversation)
    db_session.commit()

    message = Message(
        conversation_id=conversation.id,
        sender_id=user1,
        receiver_id=user2,
        content="Hello, how are you?"
    )
    db_session.add(message)
    db_session.commit()

    assert message.id is not None
    assert message.read is False
    assert message.timestamp is not None
    assert message.conversation.id == conversation.id
    assert message.content == "Hello, how are you?"


def test_conversation_has_messages(db_session):
    user1 = uuid4()
    user2 = uuid4()
    conversation = Conversation(user1_id=user1, user2_id=user2)
    db_session.add(conversation)
    db_session.commit()

    msg1 = Message(conversation_id=conversation.id, sender_id=user1, receiver_id=user2, content="Hi")
    msg2 = Message(conversation_id=conversation.id, sender_id=user2, receiver_id=user1, content="Hello")

    db_session.add_all([msg1, msg2])
    db_session.commit()

    fetched = db_session.query(Conversation).filter_by(id=conversation.id).first()
    assert len(fetched.messages) == 2
    assert {m.content for m in fetched.messages} == {"Hi", "Hello"}

# testing metrics.py
# patient metrics
def test_create_patient_metrics(db_session):
    metric = PatientMetrics(
        date=date(2024, 6, 1),
        avg_length_of_stay=5.2,
        admission_count=20
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.avg_length_of_stay == 5.2
    assert metric.admission_count == 20

# OperationalMetrics
def test_create_operational_metrics(db_session):
    metric = OperationalMetrics(
        date=date(2024, 6, 1),
        metric_name="Bed Occupancy Rate",
        value=87.5,
        unit="%"
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.metric_name == "Bed Occupancy Rate"
    assert metric.value == 87.5
    assert metric.unit == "%"
# MDTMetrics
def test_create_mdt_metrics(db_session):
    metric = MDTMetrics(
        date=date(2024, 6, 1),
        meeting_count=4,
        avg_attendance=6.75,
        avg_wait_time=2.3,
        action_completion_rate=91.0
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.meeting_count == 4
    assert metric.avg_attendance == 6.75
    assert metric.action_completion_rate == 91.0

# PathwayMetrics
def test_create_pathway_metrics(db_session):
    metric = PathwayMetrics(
        date=date(2024, 6, 1),
        avg_admission_to_treatment_days=12.4,
        readmission_rate_30d=7.2,
        no_show_rate=4.1
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.no_show_rate == 4.1

# ReferralMetrics
def test_create_referral_metrics(db_session):
    metric = ReferralMetrics(
        date=date(2024, 6, 1),
        metric_name="Referral Completion",
        value=78.5,
        unit="%"
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.metric_name == "Referral Completion"
    assert metric.unit == "%"

# ClinicianMetrics
def test_create_clinician_metrics(db_session):
    metric = ClinicianMetrics(
        date=date(2024, 6, 1),
        metric_name="Tasks Completed",
        value=95.0,
        unit="%"
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.value == 95.0

# AdminMetrics
def test_create_admin_metrics(db_session):
    metric = AdminMetrics(
        date=date(2024, 6, 1),
        metric_name="System Uptime",
        value=99.9,
        unit="%"
    )
    db_session.add(metric)
    db_session.commit()

    assert metric.id is not None
    assert metric.metric_name == "System Uptime"

# testing Organisation.py
def test_create_organisation(db_session):
    org = Organisation(name="Test Org", code="TEST123")
    db_session.add(org)
    db_session.commit()

    assert org.id is not None
    assert org.name == "Test Org"
    assert org.code == "TEST123"

# testing pathway.py
def test_create_pathway_progress(db_session):
    progress = PathwayProgress(
        patient_id=123,
        steps_total=10,
        steps_completed=7,
        status=PathwayStatusEnum.ACTIVE,
        outcome=PathwayOutcomeEnum.UNKNOWN,
        readmitted=True,
        had_complication=False,
        had_relapse=True
    )
    db_session.add(progress)
    db_session.commit()

    assert progress.id is not None
    assert progress.status == PathwayStatusEnum.ACTIVE
    assert progress.outcome == PathwayOutcomeEnum.UNKNOWN
    assert progress.readmitted is True
    assert progress.had_complication is False
    assert progress.had_relapse is True

# testing patient.py
def test_create_patient(db_session):
    patient = Patient(
        primary_guid="abc-123-xyz",
        name="Test Patient",
        admission_date=date(2024, 6, 1),
        discharge_date=date(2024, 6, 10),
        status="discharged"
    )
    db_session.add(patient)
    db_session.commit()
    assert patient.id is not None
    assert patient.primary_guid == "abc-123-xyz"
    assert patient.name == "Test Patient"
    assert patient.status == "discharged"

#  testing referrals.py
def test_create_referral(db_session):
    referral = Referral(
        patient_id=1,
        source="General Practitioner"
    )
    db_session.add(referral)
    db_session.commit()

    assert referral.id is not None
    assert referral.patient_id == 1
    assert referral.source == "General Practitioner"

# testing treatments.py
def test_create_treatment(db_session):
    treatment = Treatment(name="Physiotherapy")
    db_session.add(treatment)
    db_session.commit()

    assert treatment.id is not None
    assert treatment.name == "Physiotherapy"

def test_create_treatment_slot_booking(db_session):
    treatment = Treatment(name="Chemotherapy")
    db_session.add(treatment)
    db_session.commit()

    slot = TreatmentSlotBooking(
        treatment_id=treatment.id,
        patient_id=101,
        slot_time=datetime(2025, 6, 20, 14, 0)
    )
    db_session.add(slot)
    db_session.commit()

    assert slot.id is not None
    assert slot.treatment_id == treatment.id
    assert slot.patient_id == 101
    assert slot.slot_time == datetime(2025, 6, 20, 14, 0)
    assert slot.treatment.name == "Chemotherapy"

def getPatient(db_session):
    patient =Patient(
        primary_guid="abc-123-xyz",
        name="Test Patient",
        admission_date=date(2024, 6, 1),
        discharge_date=date(2024, 6, 10),
        status="discharged"
    )
    db_session.add(patient)
    db_session.commit()