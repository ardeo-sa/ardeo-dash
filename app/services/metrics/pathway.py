"""
This module defines functions to calculate individual metrics related to patient pathway progress,
including adherence rates, dropout rates, outcome success/failure rates, readmission rates,
admit-to-treatment times, and no-show rates.

Each metric is computed separately, and a central aggregator function compiles the results into
a dictionary keyed by metric names with associated values and units.

Requires an SQLAlchemy session to interact with the database.
"""

from sqlalchemy.orm import Session
from app.models.pathway import PathwayProgress


def calculate_pathway_adherence_rate(session: Session) -> float:
    """
    Calculates the average adherence rate to pathways.

    Returns:
        float: Average percentage of steps completed by patients.
    """
    progress = session.query(PathwayProgress).all()
    adherence_rates = [
        p.steps_completed / p.steps_total
        for p in progress
        if p.steps_total > 0
    ]
    return (sum(adherence_rates) / len(adherence_rates) * 100) if adherence_rates else 0


def calculate_pathway_dropout_rate(session: Session) -> float:
    """
    Calculates the percentage of patients who dropped out of their pathways.

    Returns:
        float: Dropout rate in percentage.
    """
    progress = session.query(PathwayProgress).all()
    if not progress:
        return 0
    dropouts = sum(1 for p in progress if p.status == "dropped")
    return (dropouts / len(progress)) * 100


def calculate_pathway_success_rate(session: Session) -> float:
    """
    Calculates the percentage of patients who successfully completed their pathways.

    Returns:
        float: Success rate in percentage.
    """
    progress = session.query(PathwayProgress).all()
    if not progress:
        return 0
    successes = sum(1 for p in progress if p.outcome == "success")
    return (successes / len(progress)) * 100


def calculate_pathway_failure_rate(session: Session) -> float:
    """
    Calculates the percentage of patients who failed their pathway.

    Returns:
        float: Failure rate in percentage.
    """
    progress = session.query(PathwayProgress).all()
    if not progress:
        return 0
    failures = sum(1 for p in progress if p.outcome == "failure")
    return (failures / len(progress)) * 100

def calculate_readmission_rate(session: Session) -> float:
    """
    Calculates the percentage of patients who were readmitted.

    Returns:
        float: Readmission rate as a percentage (0–100).
    """
    progress = session.query(PathwayProgress).all()
    if not progress:
        return 0
    readmitted = sum(1 for p in progress if getattr(p, "readmitted", False))
    return (readmitted / len(progress)) * 100


def calculate_admit_to_treatment_time(session: Session) -> float:
    """
    Calculates the average time in days from admission to treatment start.

    Returns:
        float: Average duration in days from admission to treatment.
    """
    progress = session.query(PathwayProgress).all()
    time_deltas = [
        (p.treatment_start_time - p.admission_time).days
        for p in progress
        if p.admission_time and p.treatment_start_time
    ]
    return sum(time_deltas) / len(time_deltas) if time_deltas else 0


def aggregate_pathway_metrics(session: Session) -> dict:
    """
    Aggregates all pathway-related metrics into a structured dictionary.

    Returns:
        dict: Dictionary of metric_name -> (value, unit).
    """
    return {
        "pathway_adherence_rate": (calculate_pathway_adherence_rate(session), "percent"),
        "pathway_dropout_rate": (calculate_pathway_dropout_rate(session), "percent"),
        "pathway_success_rate": (calculate_pathway_success_rate(session), "percent"),
        "pathway_failure_rate": (calculate_pathway_failure_rate(session), "percent"),
        "pathway_readmission_rate": (calculate_readmission_rate(session), "percent"),
        "pathway_admit_to_treatment_time": (calculate_admit_to_treatment_time(session), "days"),
    }
