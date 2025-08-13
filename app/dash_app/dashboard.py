"""Dash Dashboard"""
import logging
from dash import dcc, html
import pandas as pd

from sqlalchemy.exc import SQLAlchemyError

from app.database.metrics import MetricsSessionLocal
from app.models.metrics import PatientMetrics

logger = logging.getLogger(__name__)


def get_data():
    """
    Fetches patient metrics data from the metrics database and returns it as a pandas DataFrame.
    """
    logger.info("Fetching patient metrics data from metrics database.")
    try:
        with MetricsSessionLocal() as session:
            data = session.query(PatientMetrics).all()
            df = pd.DataFrame([{
                "date": m.date,
                "avg_length_of_stay": m.avg_length_of_stay,
                "admission_count": m.admission_count
            } for m in data])
            if df.empty:
                logger.warning("PatientMetrics data is empty.")
            return df
    except SQLAlchemyError as e:
        logger.exception("Failed to fetch data from metrics database %s", e)
        return pd.DataFrame()  # Return empty DataFrame to avoid crashing dashboard


def create_dashboard():
    """
    Creates a Dash HTML layout containing a graph of patient metrics over time.
    If no data is available, displays a placeholder message.
    """
    logger.info("Creating dashboard layout.")
    df = get_data()
    if df.empty:
        logger.info("No data available. Displaying placeholder message.")
        return html.Div([
            html.H1("Patient Metrics Dashboard"),
            html.P("No data available.")
        ])

    logger.info("Data available. Generating dashboard graph.")
    return html.Div([
        html.H1("Patient Metrics Dashboard"),
        dcc.Graph(
            figure={
                "data": [
                    {"x": df["date"], "y": df["avg_length_of_stay"],
                     "type": "line", "name": "Avg LOS"},
                    {"x": df["date"], "y": df["admission_count"],
                     "type": "bar", "name": "Admissions"},
                ],
                "layout": {"title": "Patient Metrics Over Time"}
            }
        )
    ])
