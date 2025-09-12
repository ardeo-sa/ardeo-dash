"""
Callbacks for the Clinician Metrics

This module defines and registers callbacks responsible for updating the
Clinician Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html, dcc
import pandas as pd
import plotly.express as px

from app.dash_app.utils.helpers import build_graph_rows, grouped_month_bar


def register_clinician_callbacks(app, data_loader):
    """
    Register callbacks related to the Clinician Metrics tab.

    Args:
        app (dash.Dash): The Dash app instance to register callbacks with.
    """

    @app.callback(
        Output('clinician-content', 'children'),
        Input('clinician-date-picker-range', 'start_date'),
        Input('clinician-date-picker-range', 'end_date')
    )
    def update_clinician_metrics(start_date, end_date):
        """
        Update the Clinician Metrics content based on the selected date range.

        Args:
            start_date (str): ISO-format start date string from the DatePickerRange.
            end_date (str): ISO-format end date string from the DatePickerRange.

        Returns:
            html.Div: The updated layout containing KPI cards and Plotly graphs.
        """
        df = data_loader('clinician_metrics_wide.csv')

        if not (start_date and end_date):
            return html.Div()

        # Filter data
        df = df[
            (df['date'] >= pd.to_datetime(start_date)) &
            (df['date'] <= pd.to_datetime(end_date))
        ]

        # Day and month columns for grouping
        df['day_of_week'] = df['date'].dt.day_name()
        df['month'] = df['date'].dt.strftime('%B')
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Figure 1: Average Count of Patients Admitted and Patients Seen by month
        fig1 = grouped_month_bar(
            df,
            columns=['avg_patients_admitted', 'avg_patients_seen'],
            month_order=month_order,
            title='Average count of patients admitted and patients seen',
            labels={
                'month': 'Month',
                'avg_patients_admitted': 'Patients admitted',
                'avg_patients_seen': 'Patients seen',
            }
        )

        # Figure 2: Average Outstanding Task Count by day of week
        grouped_df2 = df.groupby('day_of_week', as_index=False)['avg_outstanding_tasks'].mean()
        grouped_df2['day_of_week'] = pd.Categorical(grouped_df2['day_of_week'], categories=day_order, ordered=True)
        grouped_df2 = grouped_df2.sort_values('day_of_week')
        fig2 = px.line(
            grouped_df2,
            x='day_of_week',
            y='avg_outstanding_tasks',
            title='Average outstanding tasks by day of week',
        )

        # Figure 3: Patients Admitted, Patients Seen, and Outstanding tasks by day of week
        grouped_df3 = df.groupby('day_of_week', as_index=False)[
            ['avg_patients_admitted', 'avg_patients_seen', 'avg_outstanding_tasks']
        ].mean()
        grouped_df3['day_of_week'] = pd.Categorical(grouped_df3['day_of_week'], categories=day_order, ordered=True)
        grouped_df3 = grouped_df3.sort_values('day_of_week')
        fig3 = px.bar(
            grouped_df3,
            x='day_of_week',
            y=['avg_patients_admitted', 'avg_patients_seen', 'avg_outstanding_tasks'],
            barmode='group',
            title='Patients admitted, patients seen, and outstanding tasks by day of week',
            labels={
                'day_of_week': 'Day of Week',
                'avg_patients_admitted': 'Patients admitted',
                'avg_patients_seen': 'Patients seen',
                'avg_outstanding_tasks': 'Outstanding tasks',
            }
        )

        # KPI Cards + Graphs
        return html.Div([
            # KPI Row
            html.Div([
                html.Div(className='kpi-card', children=[
                    html.H4('Patients admitted'),
                    html.P(f"{df['avg_patients_admitted'].sum():.0f}")
                ]),
                html.Div(className='kpi-card', children=[
                    html.H4('Patients seen'),
                    html.P(f"{df['avg_patients_seen'].sum():.0f}")
                ]),
                html.Div(className='kpi-card', children=[
                    html.H4('Outstanding tasks'),
                    html.P(f"{df['avg_outstanding_tasks'].sum():.0f}")
                ]),
                html.Div(className='kpi-card', children=[
                    html.H4('Active clinicians'),
                    html.P(f"{df['active_clinicians'].sum():.0f}")
                ]),
            ], className='kpi-row'),

            # Graph Rows
            *build_graph_rows(fig1, fig2, fig3)
        ])
