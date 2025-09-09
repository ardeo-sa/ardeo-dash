"""
Layout configuration for the Ardeo Healthcare Dashboard.

This module defines the top-level layout of the app including
the title, dropdown menu for selecting metric categories, and
the main content container.
"""

from dash import html, dcc

def create_layout():
    """
    Create and return the top-level Dash layout.

    Returns:
        html.Div: A Div element containing the dashboard structure.
    """
    return html.Div([
        html.H1('Healthcare Metrics Dashboard', className='dashboard-title'),

        html.Div([
            html.Label('Select Metric Category:', className='dropdown-label'),
            dcc.Dropdown(
                id='dropdown-tabs',
                options=[
                    {'label': 'Operational Metrics', 'value': 'tab-1'},
                    {'label': 'Pathway Metrics', 'value': 'tab-2'},
                    {'label': 'Clinician Metrics', 'value': 'tab-3'},
                    {'label': 'Admin Metrics', 'value': 'tab-4'},
                    {'label': 'MDT Metrics', 'value': 'tab-5'},
                    {'label': 'Referral Metrics', 'value': 'tab-6'},
                ],
                value='tab-1',
                className='dropdown'
            ),
        ]),

        html.Div(id='tabs-content', className='main-content')
    ], className='main-container')
