from sqlalchemy.orm import Session

from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction, MDTCase

""" meeting details are updated to metrics database  via services #todo"""
class MdtImportService:
    def __init__(self, primary_db: Session, secondary_db: Session):
        """
        Initialize the service with primary and secondary SQLAlchemy sessions.

        Args:
            primary_db (Session): SQLAlchemy session for reading from the source (primary) DB.
            secondary_db (Session): SQLAlchemy session for writing to the target (secondary) DB.
        """
        self.primary_db = primary_db
        self.secondary_db = secondary_db
    """ Used sql because meetings are not ported yet """
    def import_mdt(self):
        meeting_map = {}
        results = (self.primary_db.execute(""" 
        SELECT m.meeting_id as meeting_id, 
        m.guid AS meeting_guid,
        m.meeting_date as meeting_date,
        m.meeting_endDate as meeting_endDate,
        atnd.attendee_user_id as attendee_user_id,
        mi.meetingitem_action_completed as meetingitem_action_completed,
        mi.subject_id as subject_id,
        mi.treatmentDecision as treatmentDecision
        FROM emdtcloud.meeting m
        LEFT JOIN meeting_item mi ON m.meeting_id = mi.meeting_id
        LEFT JOIN attendee atnd ON atnd.meeting_id = m.meeting_id; 
        """
        ).fetchall())

        for row in results:
            meeting_id = row["meeting_id"]

            # Create meeting only once
            if meeting_id not in meeting_map:
                meeting = MDTMeeting(
                    primary_guid=row["meeting_guid"],
                    meeting_start_time=row["meeting_date"],
                    meeting_end_time=row["meeting_endDate"],
                    meeting_time=(row["meeting_endDate"] - row["meeting_date"]).seconds // 60
                )
                meeting_map[meeting_id] = meeting

            meeting = meeting_map[meeting_id]

            # Add action (if exists)
            if row["meetingitem_action_completed"] is not None:
                action = MDTAction(
                    completed=row["meetingitem_action_completed"],
                    meeting=meeting
                )
                meeting.actions.append(action)

            # Add case (if exists)
            if row["subject_id"] is not None:
                case = MDTCase(
                    patient_id=row["subject_id"],
                    discussion_notes=row["treatmentDecision"],
                    meeting=meeting
                )
                meeting.cases.append(case)

            # Add participant (if exists and not already added)
            if row["attendee_user_id"] is not None:
                if not any(p.clinician_id == row["attendee_user_id"] for p in meeting.participants):
                    participant = MDTParticipant(
                        clinician_id=row["attendee_user_id"],
                        meeting=meeting
                    )
                    meeting.participants.append(participant)

        # Save all meetings and their relationships
        self.secondary_db.add_all(meeting_map.values())
        self.secondary_db.commit()