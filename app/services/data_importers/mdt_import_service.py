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
import logging
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction, MDTCase
from app.models.primary.mdt import PrimaryMDTMeeting

logger = logging.getLogger(__name__)


class MdtImportService:
    """
    Service to import MDT (Multidisciplinary Team) meeting data from an external source
    and populate it into the secondary metrics database.

    This includes meeting times, participants, patient cases, and actions derived from notes.
    """

    def __init__(self, primary_db: Session, secondary_db: Session):
        """
        Initialize the MDT import service with a database session.

        Args:
            secondary_db (Session): SQLAlchemy session used for writing to the secondary metrics database.
        """
        self.primary_db = primary_db
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
        logger.info("Starting MDT import process.")
        try:
            primary_meetings = (
                self.primary_db.query(PrimaryMDTMeeting)
                .options(
                    joinedload(PrimaryMDTMeeting.notes),
                    joinedload(PrimaryMDTMeeting.patients),
                    joinedload(PrimaryMDTMeeting.participants),
                )
                .all()
            )
            logger.debug(f"Fetched {len(primary_meetings)} MDT meetings.")
        except Exception as e:
            logger.exception("Failed to fetch MDT meetings.")
            raise

        meeting_map = {}

        for item in primary_meetings:  # list of meetings
            try:
                meeting_id = item.id
                start = item.start_time
                end = item.end_time
                duration = end - start

                # Create meeting object
                meeting = MDTMeeting(
                    primary_guid=str(meeting_id),
                    meeting_start_time=item["start_time"],
                    meeting_end_time=item["end_time"],
                    meeting_time=datetime(1970, 1, 1) + duration  # Epoch + duration for standard time format
                )
                logger.debug(f"Created MDTMeeting object for meeting_id={meeting_id}.")

                # Actions from notes
                for note in item.notes:
                    if note.content:
                        action = MDTAction(
                            completed=True,
                            meeting=meeting
                        )
                        meeting.actions.append(action)
                        logger.debug(f"Added MDTAction to meeting_id={meeting_id}.")

                # Patient cases
                for case in item.patients:
                    mdt_case = MDTCase(
                        patient_id=case.patient_id,
                        discussion_notes=None,
                        meeting=meeting
                    )
                    meeting.cases.append(mdt_case)
                    logger.debug(f"Added MDTCase for patient_id={case.patient_id} in meeting_id={meeting_id}.")

                # Participants
                for participant in item.participants:
                    clinician_id = participant.clinician_id
                    if clinician_id and not any(p.clinician_id == clinician_id for p in meeting.participants):
                        participant_obj = MDTParticipant(
                            clinician_id=clinician_id,
                            meeting=meeting
                        )
                        meeting.participants.append(participant_obj)
                        logger.debug(f"Added MDTParticipant with clinician_id={clinician_id} to meeting_id={meeting_id}.")

                meeting_map[meeting_id] = meeting

            except Exception as e:
                logger.exception(f"Error processing meeting_id={item.get('id')}. Skipping.")
                continue

        # Save all meetings and related data
        try:
            self.secondary_db.add_all(meeting_map.values())
            self.secondary_db.commit()
            logger.info(f"Successfully imported {len(meeting_map)} MDT meetings.")
        except Exception as e:
            self.secondary_db.rollback()
            logger.exception("Failed to commit MDT meetings to the secondary DB.")
            raise