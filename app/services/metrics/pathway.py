"""
This module defines a function to aggregate metrics related to patient pathway progress, including adherence rates, dropout rates,
and outcome success/failure rates. These metrics are calculated from the data stored in the `PathwayProgress` model.

Metrics aggregated:
1. **Pathway Adherence Rate**: The percentage of steps completed by patients out of total steps for their respective pathways.
2. **Pathway Dropout Rate**: The percentage of patients who dropped out of their pathway.
3. **Pathway Success Rate**: The percentage of patients who completed their pathway with a successful outcome.
4. **Pathway Failure Rate**: The percentage of patients who completed their pathway with a failed outcome.

The function requires an SQLAlchemy session to interact with the database and retrieve pathway progress data.
"""
from datetime import date
from sqlalchemy.orm import Session

from app.models.pathway import PathwayProgress

def aggregate_pathway_metrics(session: Session):
    """
    Aggregates metrics related to patient pathway progress, including adherence, dropout rates, and outcomes (success/failure).

    Args:
        session (Session): The SQLAlchemy session to query the database.

    Returns:
        List[Tuple[str, float, str]]: A list of tuples where each tuple contains the metric name, its value, and its unit of measurement.
            Example:
            [
                ("pathway_adherence_rate", 75.5, "percent"),
                ("pathway_dropout_rate", 10.0, "percent"),
                ("pathway_success_rate", 80.0, "percent"),
                ("pathway_failure_rate", 20.0, "percent")
            ]
    """
    today = date.today()

    progress = session.query(PathwayProgress).all()

    # Adherence = completed_steps / total_steps
    adherence_rates = [
        p.steps_completed / p.steps_total
        for p in progress
        if p.steps_total > 0
    ]
    avg_adherence = sum(adherence_rates) / len(adherence_rates) * 100 if adherence_rates else 0

    # Dropouts
    dropouts = sum(1 for p in progress if p.status == "dropped")
    dropout_rate = (dropouts / len(progress)) * 100 if progress else 0

    # Outcomes
    success_rate = sum(1 for p in progress if p.outcome == "success") / len(progress) * 100 if progress else 0
    failure_rate = sum(1 for p in progress if p.outcome == "failure") / len(progress) * 100 if progress else 0

    return [
        ("pathway_adherence_rate", avg_adherence, "percent"),
        ("pathway_dropout_rate", dropout_rate, "percent"),
        ("pathway_success_rate", success_rate, "percent"),
        ("pathway_failure_rate", failure_rate, "percent"),
    ]
