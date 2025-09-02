"""Data loading module"""
import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.database.metrics import MetricsSessionLocal
from app.models.reporting.metrics import PatientMetrics
from app.dash_app.utils.data_loader import load_data

logger = logging.getLogger(__name__)


def get_real_data():
    """Fetch patient metrics data from DB."""
    try:
        with MetricsSessionLocal() as session:
            data = session.query(PatientMetrics).all()
            df = pd.DataFrame([{
                "date": m.date,
                "avg_length_of_stay": m.avg_length_of_stay,
                "admission_count": m.admission_count
            } for m in data])
            if df.empty:
                logger.warning("DB returned no rows.")
            return df
    except SQLAlchemyError as e:
        logger.exception("DB fetch failed: %s", e)
        return pd.DataFrame()


def get_data_loader(source: str):
    """
    Returns a data loader function based on source.
    Used to inject into callbacks so they don’t care about the backend.
    - In 'real' mode, always return DB data (ignores file_path).
    - In 'synthetic' mode, load CSV from the given file_path.
    """
    if source == "real":
        return lambda _: get_real_data()
    else:
        return lambda file_path: load_data(file_path)
