"""
This module provides functionality to import MDT (Multidisciplinary Team) meeting data
into the metrics database.

The main service, `MdtImportService`, fetches raw meeting records from an external source
(via `fetch_meetings`) and processes the following entities:

- `MDTMeeting`: Stores metadata about each MDT session.
- `MDTParticipant`: Links clinicians to meetings they participated in.
- `MDTCase`: Records patient cases discussed during the meeting.
- `MDTAction`: Captures any follow-up actions noted in the meeting (derived from notes).

The service is designed to work with a secondary SQLAlchemy session, committing all entities
in one transaction to ensure data consistency.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction, MDTCase
from app.services.meeting_services import fetch_meetings


class MdtImportService:
    """
    Service to import MDT (Multidisciplinary Team) meeting data from an external source
    and populate it into the secondary metrics database.

    This includes meeting times, participants, patient cases, and actions derived from notes.
    """

    def __init__(self, secondary_db: Session):
        """
        Initialize the MDT import service with a database session.

        Args:
            secondary_db (Session): SQLAlchemy session used for writing to the secondary metrics database.
        """
        self.secondary_db = secondary_db

    def import_mdt(self):
        """
        Imports MDT meeting data using the `fetch_meetings()` service and saves it to the secondary database.

        Each meeting may contain:
        - Start and end time with calculated duration
        - Actions inferred from meeting notes
        - Cases linked to patients discussed in the meeting
        - Participants (clinicians)

        All entities are mapped and committed in a single transaction.
        """
        meeting_map = {}
        results = fetch_meetings()

        for item in results:  # list of meetings
            meeting_id = item["id"]
            start = datetime.fromisoformat(item["start_time"])
            end = datetime.fromisoformat(item["end_time"])
            duration = end - start

            # Create meeting object
            meeting = MDTMeeting(
                primary_guid=str(meeting_id),
                meeting_start_time=item["start_time"],
                meeting_end_time=item["end_time"],
                meeting_time=datetime(1970, 1, 1) + duration  # Epoch + duration for standard time format
            )
            meeting_map[meeting_id] = meeting

            # Add actions from notes
            for note in item.get("notes", []):
                if note.get("content"):
                    action = MDTAction(
                        completed=True,
                        meeting=meeting
                    )
                    meeting.actions.append(action)

            # Add patient cases
            for patient in item.get("patients", []):
                case = MDTCase(
                    patient_id=patient["id"],
                    discussion_notes=None,
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

        # Save all meetings and related data
        self.secondary_db.add_all(meeting_map.values())
        self.secondary_db.commit()
