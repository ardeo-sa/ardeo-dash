"""
This module defines metrics related to patient referrals, including source breakdowns,
conversion rates, referral-to-admission time, and referral volume trends over time.
"""
import logging
from datetime import date
# from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.admissions import ReferralAdmission

logger = logging.getLogger(__name__)

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
    logger.debug(f"Fetching referrals by source for {for_date}")

    results = (
        session.query(
            ReferralAdmission.referral_source,
            func.count(ReferralAdmission.id).label("count") # pylint: disable=not-callable
        )
        .filter(func.date(ReferralAdmission.referral_time) == for_date)
        .group_by(ReferralAdmission.referral_source)
        .all() # pylint: disable=not-callable
    )
    source_counts = dict(results)
    logger.info(f"Referral counts by source on {for_date}: {source_counts}")
    return source_counts


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
    logger.debug(f"Calculating referral conversion rate for {for_date}")

    total_referrals = session.query(ReferralAdmission).filter(
        func.date(ReferralAdmission.referral_time) == for_date
    ).count()

    admitted = session.query(ReferralAdmission).filter(
        func.date(ReferralAdmission.referral_time) == for_date,
        ReferralAdmission.admission_time.isnot(None)
    ).count()

    rate = (admitted / total_referrals) * 100
    logger.info(f"Referral conversion rate for {for_date}: {rate:.2f}%")
    return rate


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
    logger.debug(f"Calculating referral-to-admission time for {for_date}")

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

    if not time_deltas:
        logger.warning(f"No completed referrals found for {for_date}. Returning 0 days.")
        return 0

    average_time = sum(time_deltas) / len(time_deltas)
    logger.info(f"Average referral-to-admission time for {for_date}: {average_time:.2f} days")
    return average_time


def referral_volume_trend(session: Session, by: str = "day") -> dict:
    """
    Returns referral counts grouped by day, week, or month.

    Args:
        session (Session): SQLAlchemy session.
        by (str): One of 'day', 'week', 'month'.

    Returns:
        dict: {(year, period): count}
    """
    logger.debug(f"Fetching referral volume trend grouped by '{by}'")

    if by == "day":
        group_expr = func.date(ReferralAdmission.referral_time)
    elif by == "week":
        group_expr = (extract("year", ReferralAdmission.referral_time),
                      extract("week", ReferralAdmission.referral_time))
    elif by == "month":
        group_expr = (extract("year", ReferralAdmission.referral_time),
                      extract("month", ReferralAdmission.referral_time))
    else:
        logger.error(f"Invalid 'by' parameter: {by}")
        raise ValueError("Invalid 'by' value. Choose from 'day', 'week', 'month'.")

    results = (
        session.query(group_expr, func.count(ReferralAdmission.id)) # pylint: disable=not-callable
        .group_by(group_expr)
        .all() # pylint: disable=not-callable
    )

    trend = {
        tuple(row[0]) if isinstance(row[0], tuple) else row[0]: row[1]
        for row in results
    }

    logger.info(f"Referral volume trend ({by}): {trend}")
    return trend


def aggregate_referral_metrics(session: Session, for_date: date = None) -> dict:
    """
    Aggregates all referral-related metrics into a structured dictionary.

    Args:
        session (Session): SQLAlchemy session.
        for_date (date, optional): Date to filter the metrics. Defaults to today.

    Returns:
        dict: Dictionary of metric_name -> (value, unit).
    """
    for_date = for_date or date.today()
    logger.info(f"Aggregating referral metrics for {for_date}")

    metrics = {}

    try:
        # Referral source breakdown
        referrals_by_src = referrals_by_source(session, for_date)

        # Add individual referral source counts
        for source, count in referrals_by_src.items():
            metric_name = f"referral_source_count_{source.lower().replace(' ', '_')}"
            metrics[metric_name] = (count, "count")

        # metrics.update({
        #     f"referral_source_count_{source.lower().replace(' ', '_')}": (count, "count")
        #     for source, count in referrals_by_src.items()
        # })

        # Aggregate metrics
        conversion = referral_conversion_rate(session, for_date)
        metrics["referral_conversion_rate"] = (conversion, "percent")

        referral_time = referral_to_admission_time(session, for_date)
        metrics["referral_to_admission_time"] = (referral_time, "days")

        # Add referral volume trend by day
        daily_trend = referral_volume_trend(session, by="day")
        daily_key = for_date.isoformat()
        if daily_key in daily_trend:
            metrics["referral_volume_daily"] = (daily_trend[daily_key], "count")

        logger.info(f"Aggregated referral metrics for {for_date}: {metrics}")

    except Exception as e:
        logger.exception(f"Error while aggregating referral metrics for {for_date}: {e}")

    return metrics
