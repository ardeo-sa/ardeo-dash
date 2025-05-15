"""
This module defines metrics related to patient referrals, including source breakdowns,
conversion rates, referral-to-admission time, and referral volume trends over time.
"""
from datetime import date
from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, extract

from app.models.admissions import ReferralAdmission


def referrals_by_source(session: Session, for_date: date = None) -> dict:
    """
    Returns the count of referrals by source for a given day.

    Args:
        session (Session): SQLAlchemy session.
        for_date (date, optional): Date to filter referrals. Defaults to today.

    Returns:
        dict: source -> count
    """
    for_date = for_date or date.today()
    results = (
        session.query(
            ReferralAdmission.referral_source,
            func.count(ReferralAdmission.id)
        )
        .filter(func.date(ReferralAdmission.referral_time) == for_date)
        .group_by(ReferralAdmission.referral_source)
        .all()
    )
    return {source: count for source, count in results}


def referral_conversion_rate(session: Session, for_date: date = None) -> float:
    """
    Calculates the percentage of referrals that resulted in an admission.

    Args:
        session (Session): SQLAlchemy session.
        for_date (date, optional): Date to filter. Defaults to today.

    Returns:
        float: Conversion rate in percent.
    """
    for_date = for_date or date.today()
    total_referrals = session.query(ReferralAdmission).filter(
        func.date(ReferralAdmission.referral_time) == for_date
    ).count()

    admitted = session.query(ReferralAdmission).filter(
        func.date(ReferralAdmission.referral_time) == for_date,
        ReferralAdmission.admission_time.isnot(None)
    ).count()

    return (admitted / total_referrals * 100) if total_referrals else 0


def referral_to_admission_time(session: Session, for_date: date = None) -> float:
    """
    Calculates the average time (in days) from referral to admission.

    Args:
        session (Session): SQLAlchemy session.
        for_date (date, optional): Filter referrals by date. Defaults to today.

    Returns:
        float: Average time in days.
    """
    for_date = for_date or date.today()
    rows = session.query(
        ReferralAdmission.referral_time,
        ReferralAdmission.admission_time
    ).filter(
        func.date(ReferralAdmission.referral_time) == for_date,
        ReferralAdmission.admission_time.isnot(None)
    ).all()

    time_deltas = [
        (admit - referral).days
        for referral, admit in rows
        if referral and admit
    ]

    return sum(time_deltas) / len(time_deltas) if time_deltas else 0


def referral_volume_trend(session: Session, by: str = "day") -> dict:
    """
    Returns referral counts grouped by day, week, or month.

    Args:
        session (Session): SQLAlchemy session.
        by (str): One of 'day', 'week', 'month'.

    Returns:
        dict: {(year, period): count}
    """
    if by == "day":
        group_expr = func.date(ReferralAdmission.referral_time)
    elif by == "week":
        group_expr = (extract("year", ReferralAdmission.referral_time), extract("week", ReferralAdmission.referral_time))
    elif by == "month":
        group_expr = (extract("year", ReferralAdmission.referral_time), extract("month", ReferralAdmission.referral_time))
    else:
        raise ValueError("Invalid 'by' value. Choose from 'day', 'week', 'month'.")

    results = (
        session.query(group_expr, func.count(ReferralAdmission.id))
        .group_by(group_expr)
        .all()
    )

    return {tuple(row[0]) if isinstance(row[0], tuple) else row[0]: row[1] for row in results}
