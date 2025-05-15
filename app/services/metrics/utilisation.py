"""
This module contains the `store_metrics` function that aggregates various metrics (operational, MDT, pathway, and utilization)
and stores them in the `OperationalMetrics` table of the metrics database. The metrics are gathered from different modules
such as `operational`, `mdt`, `pathway`, and `utilization`.

The function aggregates the following metrics:
1. **Operational Metrics**: Metrics related to hospital operations such as admissions, discharges, etc.
2. **MDT Metrics**: Metrics related to MDT (Multi-Disciplinary Team) meetings and actions.
3. **Pathway Metrics**: Metrics related to patient pathways such as adherence, success, and failure rates.
4. **Utilization Metrics**: Metrics related to the utilization of hospital resources.

The aggregated metrics are then saved in the `OperationalMetrics` table with the current date.
"""
from datetime import date

from app.services.metrics.utilization import aggregate_utilization_metrics
from app.database.metrics import MetricsSessionLocal
from app.models.metrics import OperationalMetrics
from app.services.metrics.mdt import aggregate_mdt_metrics
from app.services.metrics.operational import aggregate_operational_metrics
from app.services.metrics.pathway import aggregate_pathway_metrics

def store_metrics():
    """
    Aggregates various metrics (operational, MDT, pathway, and utilization) and stores them in the `OperationalMetrics` table.

    This function aggregates metrics from the following sources:
    - Operational metrics (e.g., daily admissions, length of stay, etc.)
    - MDT (Multi-Disciplinary Team) metrics (e.g., meeting attendance, action completion rate)
    - Pathway metrics (e.g., adherence rate, success/failure rate)
    - Utilization metrics (e.g., resource usage)

    The metrics are then stored in the metrics database with the current date.

    Args:
        None

    Returns:
        None
    """
    today = date.today()
    with MetricsSessionLocal() as session:
        all_metrics = []
        all_metrics += aggregate_operational_metrics(session)
        all_metrics += aggregate_mdt_metrics(session)
        all_metrics += aggregate_pathway_metrics(session)
        all_metrics += aggregate_utilization_metrics(session)

        for name, value, unit in all_metrics:
            session.add(OperationalMetrics(date=today, metric_name=name, value=value, unit=unit))
        session.commit()
