"""
This module defines the functions that calculates metrics related to MDT meetings.
These metrics include the total number of meetings, average attendance, average wait time from referral to MDT meeting,
and action completion rate.

The function uses SQLAlchemy queries to retrieve and calculate the required metrics from the database.
It returns the results as a list of tuples, each containing the metric name, value, and unit of measurement.

Metrics calculated:
1. MDT Meeting Count: Total number of MDT meetings held today.
2. MDT Average Attendance: Average number of participants attending MDT meetings.
3. MDT Average Wait Time: Average time (in days) between referral and review in MDT meetings.
4. MDT Action Completion Rate: Percentage of MDT actions that have been completed.

The function expects an active SQLAlchemy session to query the database.
"""

from datetime import date
from typing import Dict, Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction


def calculate_mdt_meeting_count(session: Session, for_date: date = None) -> int:
    """
    Computes mdt meeting count
    """
    for_date = for_date or date.today()
    return session.query(MDTMeeting).filter(func.date(MDTMeeting.meeting_time) == for_date).count()


def calculate_mdt_avg_attendance(session: Session) -> float:
    """
    Computes the average number of participants across all MDT meetings.
    """
    meeting_ids = session.query(MDTMeeting.id).all()
    if not meeting_ids:
        return 0

    total_attendance = 0
    for (meeting_id,) in meeting_ids:
        count = session.query(MDTParticipant).filter(MDTParticipant.meeting_id == meeting_id).count()
        total_attendance += count

    return total_attendance / len(meeting_ids)


def calculate_mdt_avg_wait_time(session: Session) -> float:
    """
    Computes the average number of days between referral and review in MDT meetings.
    """
    meetings = session.query(MDTMeeting).filter(
        MDTMeeting.referral_time.isnot(None),
        MDTMeeting.review_time.isnot(None)
    ).all()
    wait_times = [(m.review_time - m.referral_time).days for m in meetings]
    return sum(wait_times) / len(wait_times) if wait_times else 0


def calculate_mdt_action_completion_rate(session: Session) -> float:
    """
    Calculates the percentage of MDT actions that have been marked as completed.
    """
    actions = session.query(MDTAction).all()
    if not actions:
        return 0

    completed = sum(1 for action in actions if action.completed)
    return (completed / len(actions)) * 100


def calculate_mdt_avg_case_discussion_time(session: Session) -> float:
    """
    Calculates the average time (in minutes) spent discussing each case during MDT meetings.

    Returns:
        float: Average time per case in minutes.
    """
    meetings = session.query(MDTMeeting).filter(
        MDTMeeting.meeting_start_time.isnot(None),
        MDTMeeting.meeting_end_time.isnot(None),
        MDTMeeting.cases.any()
    ).all()

    total_minutes = 0
    total_cases = 0

    for meeting in meetings:
        duration = (meeting.meeting_end_time - meeting.meeting_start_time).total_seconds() / 60
        case_count = len(meeting.cases)

        if case_count > 0:
            total_minutes += duration
            total_cases += case_count

    return (total_minutes / total_cases) if total_cases > 0 else 0


def aggregate_mdt_metrics(session: Session, for_date: date = None) -> Dict[str, Any]:
    """
    Aggregates all MDT metrics and returns them as a dictionary.
    """
    for_date = for_date or date.today()

    return {
        "date": for_date,
        "mdt_meeting_count": calculate_mdt_meeting_count(session, for_date),
        "mdt_avg_attendance": calculate_mdt_avg_attendance(session),
        "mdt_avg_wait_time": calculate_mdt_avg_wait_time(session),
        "mdt_action_completion_rate": calculate_mdt_action_completion_rate(session),
        "mdt_avg_case_discussion_time": calculate_mdt_avg_case_discussion_time(session),
    }
