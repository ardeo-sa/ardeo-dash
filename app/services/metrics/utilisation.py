from datetime import date

from app.services.metrics.utilization import aggregate_utilization_metrics

from app.database.metrics import MetricsSessionLocal
from app.models.metrics import OperationalMetrics
from app.services.metrics.mdt import aggregate_mdt_metrics
from app.services.metrics.operational import aggregate_operational_metrics
from app.services.metrics.pathway import aggregate_pathway_metrics


def store_metrics():
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
