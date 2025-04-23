# app/services/metrics/pathway.py

from sqlalchemy.orm import Session
from datetime import date
from app.models.pathway import PathwayProgress
from app.models.metrics import OperationalMetrics

def aggregate_pathway_metrics(session: Session):
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
