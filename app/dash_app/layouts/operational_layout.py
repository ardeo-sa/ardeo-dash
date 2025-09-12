"""
Layout definition for the Operational Metrics tab.
"""

from dash import html
from app.dash_app.utils.data_loader import load_data
from app.dash_app.layouts.helpers import date_picker_container

def operational_layout():
    """
    Create the layout for the Operational Metrics tab.

    Returns:
        html.Div: Layout containing date picker and content container.
    """
    df = load_data('operational_metrics_wide.csv')
    return html.Div([
        html.H3('Select Date Range', className='date-range-title'),
        date_picker_container(df, picker_id='operational-date-picker-range'),
        html.Div(id='operational-content')
    ])
