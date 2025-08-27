"""
Layout definition for the Pathway Metrics tab.
"""

from dash import html, dcc
from ..utils.data_loader import load_data

def pathway_layout():
    """
    Create the layout for the Pathway Metrics tab.

    Returns:
        html.Div: Layout containing date picker and content container.
    """
    df = load_data('pathway_metrics_wide.csv')
    return html.Div([
        html.Div([
            html.H3('Select Date Range', className='date-range-title'),
            dcc.DatePickerRange(
                id='pathway-date-picker-range',
                min_date_allowed=df['date'].min(),
                max_date_allowed=df['date'].max(),
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD',
                className='date-picker'
            ),
        ], className='date-picker-container'),
        html.Div(id='pathway-content')
    ])
