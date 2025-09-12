# pylint: disable=R0801
"""
Callbacks for the Referral Metrics

This module defines and registers callbacks responsible for updating the
Referral Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html
from app.dash_app.utils.helpers import build_graph_rows, grouped_month_bar, load_and_filter


def register_referral_callbacks(app, data_loader):
    """
    Register callbacks related to the Admin Metrics tab.

    Args:
        app (dash.Dash): The Dash app instance to register callbacks with.
    """

    @app.callback(
        Output('referral-content', 'children'),
        Input('referral-date-picker-range', 'start_date'),
        Input('referral-date-picker-range', 'end_date')
    )
    def update_referral_metrics(start_date, end_date):
        """
        Update the Referral Metrics content based on the selected date range.

        This callback reads data from 'referral_metrics_wide.csv', filters
        it by the provided date range, and generates KPI cards and multiple
        graphs showing trends and averages.

        Args:
            start_date (str): ISO-format start date string from the DatePickerRange.
            end_date (str): ISO-format end date string from the DatePickerRange.

        Returns:
            html.Div: The updated layout containing KPI cards and Plotly graphs.
        """
        df = load_and_filter(
            data_loader,
            'operational_metrics_wide.csv',
            start_date,
            end_date,
            add_day=True,
            add_month=True
        )
        if df is None:
            return html.Div()

        # --- Figure 1: Referral Volume + Conversion Rate by month ---
        fig1 = grouped_month_bar(
            df,
            columns=['referral_volume_daily', 'referral_conversion_rate'],
            title='Referral volume and referral conversion rate',
            labels={'value': 'Rate (%)', 'month': 'Month', 'variable': 'Metric'}
        )

        # KPI cards + Graphs
        return html.Div([
            # KPI Row
            html.Div([
                html.Div(className='kpi-card', children=[html.H4('Avg referral to admission time (days)'),
                                                         html.P(f"{df['referral_to_admission_time'].mean():.2f}")]),
                html.Div(className='kpi-card', children=[html.H4('Referral volume'),
                                                         html.P(f"{df['referral_volume_daily'].sum()}")]),
                html.Div(className='kpi-card', children=[html.H4('Referral source'),
                                                         html.P(f"{df['referral_source_count'].sum()}")]),
            ], className='kpi-row'),

            # Graph Rows
            *build_graph_rows(fig1)
        ])
