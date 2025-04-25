# app/services/metrics/mdt.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.mdt import MDTMeeting, MDTParticipant, MDTAction
from app.models.metrics import OperationalMetrics

def aggregate_mdt_metrics(session: Session):
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
