"""
Layout definition for the Clinician Metrics tab.
"""

from dash import html, dcc
from utils.data_loader import load_data

def mdt_layout():
    """
    Create the layout for the MDT Metrics tab.

    Returns:
        html.Div: Layout containing date picker and content container.
    """
    df = load_data('data/mdt_metrics_wide.csv')
    return html.Div([
        html.Div([
            html.H3('Select Date Range', className='date-range-title'),
            dcc.DatePickerRange(
                id='mdt-date-picker-range',
                min_date_allowed=df['date'].min(),
                max_date_allowed=df['date'].max(),
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD',
                className='date-picker'
            ),
        ], className='date-picker-container'),
        html.Div(id='mdt-content')
    ])