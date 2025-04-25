
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sqlalchemy.orm import Session
from app.database.metrics import MetricsSessionLocal
from app.models.metrics import PatientMetrics

def get_data():
    with MetricsSessionLocal() as session:
        data = session.query(PatientMetrics).all()
        return pd.DataFrame([{
            "date": m.date,
            "avg_length_of_stay": m.avg_length_of_stay,
            "admission_count": m.admission_count
        } for m in data])

def create_dashboard():
    df = get_data()
    if df.empty:
        return html.Div([
            html.H1("Patient Metrics Dashboard"),
            html.P("No data available.")
        ])
    return html.Div([
        html.H1("Patient Metrics Dashboard"),
        dcc.Graph(
            figure={
                "data": [
                    {"x": df["date"], "y": df["avg_length_of_stay"], "type": "line", "name": "Avg LOS"},
                    {"x": df["date"], "y": df["admission_count"], "type": "bar", "name": "Admissions"},
                ],
                "layout": {"title": "Patient Metrics Over Time"}
            }
        )
    ])
