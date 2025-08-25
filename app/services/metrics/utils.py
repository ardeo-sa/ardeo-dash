"""
This module provides utility functions for calculating time-based metrics
between two datetime fields in SQLAlchemy models.

It currently includes:

- avg_days_between: Computes the average number of days between two datetime
  attributes across all records in a given model.

Requires an SQLAlchemy session to query the database.
"""
import logging
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def avg_days_between(session: Session, model, start_attr: str, end_attr: str) -> float:
    """
    Computes the average number of days between two datetime attributes in a model.
    """
    records = session.query(model).filter(
        getattr(model, start_attr).isnot(None),
        getattr(model, end_attr).isnot(None)
    ).all()

    if not records:
        logger.debug("No records found for average days calculation (%s -> %s)", start_attr, end_attr)
        return 0.0

    total_days = sum((getattr(r, end_attr) - getattr(r, start_attr)).days for r in records)
    avg = total_days / len(records)
    logger.debug("Average days between %s and %s: %.2f (across %d records)",
                 start_attr, end_attr, avg, len(records))
    return avg
