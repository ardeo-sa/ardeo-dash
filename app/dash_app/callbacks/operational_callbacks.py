# pylint: disable=R0801
"""
Callbacks for the Operational Metrics

This module defines and registers callbacks responsible for updating the
Operational Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""
from dash import Output, Input, html
import plotly.express as px
from app.dash_app.utils.helpers import build_graph_rows, grouped_day_bar, load_and_filter


def register_operational_callbacks(app, data_loader):
    """
    Register callbacks related to the Operational Metrics tab.

    Args:
        app (dash.Dash): The Dash app instance to register callbacks with.
    """

    @app.callback(
        Output('operational-content', 'children'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    )
    def update_operational_metrics(start_date, end_date):
        """
        Update the Operational Metrics content based on the selected date range.

        This callback reads data from 'operational_metrics_wide.csv', filters
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

        # day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # --- Figure 1: No-show rate ---
        fig1 = grouped_day_bar(
            df,
            columns=['appointment_no_show_rate'],
            title='Average appointment no-show rate by day of week',
            labels={'day_of_week': 'Day of Week', 'appointment_no_show_rate': 'No-show Rate (%)'},
            barmode=None
        )

        # --- Figure 2: Admissions + Discharges ---
        fig2 = grouped_day_bar(
            df,
            columns=['daily_admissions', 'daily_discharges'],
            title='Average admissions and discharges by day of week',
            labels={
                'day_of_week': 'Day of Week',
                'daily_admissions': 'Admissions',
                'daily_discharges': 'Discharges'
            }
        )

        # Figure 3: MDT wait time
        fig3 = px.bar(df, x='date', y='average_mdt_wait_time', title='Avg MDT wait time by day')

        # Figure 4: Admissions to treatment start and length of stay
        fig4 = px.line(
            df,
            x='date',
            y=['admission_to_treatment_start', 'average_length_of_stay'],
            title='Admissions to treatment start and length of stay'
        )

        # KPI cards + Graphs
        return html.Div([
            # KPI Row
            html.Div([
                html.Div(className='kpi-card', children=[html.H4('Admissions'),
                                                         html.P(f"{df['daily_admissions'].sum()}")]),
                html.Div(className='kpi-card', children=[html.H4('Discharges'),
                                                         html.P(f"{df['daily_discharges'].sum()}")]),
                html.Div(className='kpi-card', children=[html.H4('Bed Occupancy'),
                                                         html.P(f"{df['bed_occupancy_rate'].mean() / 100:.2%}")]),
                html.Div(className='kpi-card', children=[html.H4('Readmission Rate'),
                                                         html.P(f"{df['readmission_rate_30d'].mean() / 100:.2%}")]),
            ], className='kpi-row'),

            # Graph Rows
            *build_graph_rows(fig1, fig2, fig3, fig4) # pylint: disable=E1121
        ])
