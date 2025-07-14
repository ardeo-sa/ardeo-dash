from datetime import datetime

from sqlalchemy.orm import Session

from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction, MDTCase
from app.services.meeting_services import fetch_meetings

""" meeting details are updated to metrics database  via services #todo"""
class MdtImportService:
    def __init__(self, secondary_db: Session):
        """
        Initialize the service with primary and secondary SQLAlchemy sessions.

        Args:
            secondary_db (Session): SQLAlchemy session for writing to the target (secondary) DB.
        """
        self.secondary_db = secondary_db
    """ Used sql because meetings are not ported yet """
    def import_mdt(self):
        meeting_map = {}
        results = fetch_meetings()

        for item in results:  # list of meetings
            meeting_id = item["id"]
            start = datetime.fromisoformat(item["start_time"])
            end = datetime.fromisoformat(item["end_time"])
            duration = end - start
            # Create meeting object
            meeting = MDTMeeting(
                primary_guid=str(meeting_id),  # Assuming you use the ID as the GUID here
                meeting_start_time=item["start_time"],
                meeting_end_time=item["end_time"],
                # Convert duration to datetime by adding to epoch
                 meeting_time = datetime(1970, 1, 1) + duration
            )
            meeting_map[meeting_id] = meeting

            # Add actions based on notes (assumption: using 'notes' as actions)
            for note in item.get("notes", []):
                if note.get("content"):
                    action = MDTAction(
                        # could not be determined at the moment so set to true
                        # completed=note["content"],
                        completed=True,
                        meeting=meeting
                    )
                    meeting.actions.append(action)

            # Add cases from patients
            for patient in item.get("patients", []):
                case = MDTCase(
                    patient_id=patient["id"],
                    discussion_notes=None,  # You can pick a relevant note to assign if needed
                    meeting=meeting
                )
                meeting.cases.append(case)

            # Add participants
            for participant in item.get("participants", []):
                user_id = participant.get("id")
                if user_id and not any(p.clinician_id == user_id for p in meeting.participants):
                    participant_obj = MDTParticipant(
                        clinician_id=user_id,
                        meeting=meeting
                    )
                    meeting.participants.append(participant_obj)

        # Save all meetings and their relationships
        self.secondary_db.add_all(meeting_map.values())
        self.secondary_db.commit()