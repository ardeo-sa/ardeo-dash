# pylint: disable=R0801
"""
Callbacks for the Pathway Metrics

This module defines and registers callbacks responsible for updating the
Pathway Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html
import plotly.express as px
# from utils.data_loader import load_data
from app.dash_app.utils.helpers import build_graph_rows, grouped_month_bar, load_and_filter


def register_pathway_callbacks(app, data_loader):
    """
    Register callbacks related to the Pathway Metrics tab.

    Args:
        app (dash.Dash): The Dash app instance to register callbacks with.
    """

    @app.callback(
        Output('pathway-content', 'children'),
        Input('pathway-date-picker-range', 'start_date'),
        Input('pathway-date-picker-range', 'end_date')
    )
    def update_pathway_metrics(start_date, end_date):
        """
        Update the Pathway Metrics content based on the selected date range.

        This callback reads data from 'pathway_metrics_wide.csv', filters
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
            'pathway_metrics_wide.csv',
            start_date,
            end_date,
            add_day=True,
            add_month=True
        )
        if df is None:
            return html.Div()

        # --- Figure 1: Dropout vs adherence by month ---
        fig1 = grouped_month_bar(
            df,
            columns=['pathway_adherence_rate', 'pathway_dropout_rate'],
            title='Avg dropout and adherence rate',
            labels={'value': 'Rate (%)', 'month': 'Month', 'variable': 'Metric'}
        )

        # --- Figure 2: Treatment duration over time (daily line) ---
        fig2 = px.line(
            df,
            x='date',
            y='pathway_treatment_duration',
            title='Avg treatment duration',
            labels={'pathway_treatment_duration': 'Days', 'date': 'Date'}
        )

        # --- Figure 3: Relapse vs readmission by month ---
        fig3 = grouped_month_bar(
            df,
            columns=['pathway_relapse_rate', 'pathway_readmission_rate'],
            title='Avg relapse and readmission rate',
            labels={'value': 'Rate (%)', 'month': 'Month', 'variable': 'Metric'}
        )

        # KPI cards + Graphs
        return html.Div([
            # KPI Row
            html.Div([
                html.Div(className='kpi-card', children=[html.H4('Success rate'),
                                                html.P(f"{df['pathway_success_rate'].mean() / 100:.2%}")]),
                html.Div(className='kpi-card', children=[html.H4('Failure rate'),
                                                html.P(f"{df['pathway_failure_rate'].mean() / 100:.2%}")]),
                html.Div(className='kpi-card', children=[html.H4('Complication rate'),
                                                html.P(f"{df['pathway_complication_rate'].mean() / 100:.2%}")]),
                html.Div(className='kpi-card', children=[html.H4('Adherence rate'),
                                                html.P(f"{df['pathway_adherence_rate'].mean() / 100:.2%}")]),
            ], className='kpi-row'),

            # Graph Rows
            *build_graph_rows(fig1, fig2, fig3)
        ])
