"""
This module defines the `aggregate_mdt_metrics` function that aggregates various metrics related to MDT (Multidisciplinary Team) meetings.
These metrics include the total number of meetings, average attendance, average wait time from referral to MDT meeting,
and action completion rate.

The function uses SQLAlchemy queries to retrieve and calculate the required metrics from the database.
It returns the results as a list of tuples, each containing the metric name, value, and unit of measurement.

Metrics aggregated:
1. **MDT Meeting Count**: Total number of MDT meetings held today.
2. **MDT Average Attendance**: Average number of participants attending MDT meetings.
3. **MDT Average Wait Time**: Average time (in days) between referral and review in MDT meetings.
4. **MDT Action Completion Rate**: Percentage of MDT actions that have been completed.

The function expects an active SQLAlchemy session to query the database.
"""
from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction


def aggregate_mdt_metrics(session: Session):
    """
    Aggregates MDT-related metrics from the database for the current day.

    The function calculates the following metrics:
    1. **MDT Meeting Count**: Total number of MDT meetings held today.
    2. **MDT Average Attendance**: Average number of participants attending MDT meetings.
    3. **MDT Average Wait Time**: Average time (in days) between the referral and review time for MDT meetings.
    4. **MDT Action Completion Rate**: Percentage of MDT actions that have been completed.

    The function performs the following:
    1. Fetches data related to MDT meetings, participants, and actions from the database.
    2. Computes the required metrics.
    3. Returns the metrics as a list of tuples, each containing the metric name, value, and unit of measurement.

    Args:
        session (Session): The SQLAlchemy session to use for querying the database.

    Returns:
        List[Tuple[str, float, str]]: A list of tuples, each representing a metric with its name, value, and unit.
    """
    today = date.today()

    total_meetings = session.query(MDTMeeting).filter(
        func.date(MDTMeeting.meeting_time) == today
    ).count()

    avg_attendance = session.query(func.avg(
        session.query(MDTParticipant)
        .filter(MDTParticipant.meeting_id == MDTMeeting.id)
        .correlate(MDTMeeting)
        .count()
    )).scalar() or 0

    # Time from referral to MDT
    wait_durations = session.query(MDTMeeting).filter(
        MDTMeeting.referral_time.isnot(None),
        MDTMeeting.review_time.isnot(None)
    ).all()
    wait_times = [(m.review_time - m.referral_time).days for m in wait_durations]
    avg_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0

    # Action completion rate
    actions = session.query(MDTAction).all()
    if actions:
        completed = sum(1 for a in actions if a.completed)
        completion_rate = (completed / len(actions)) * 100
    else:
        completion_rate = 0

    return [
        ("mdt_meeting_count", total_meetings, "count"),
        ("mdt_avg_attendance", avg_attendance, "people"),
        ("mdt_avg_wait_time", avg_wait_time, "days"),
        ("mdt_action_completion_rate", completion_rate, "percent"),
    ]
