"""
Callbacks for the Operational Metrics

This module defines and registers callbacks responsible for updating the
Operational Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html, dcc
import pandas as pd
import plotly.express as px
# from utils.data_loader import load_data


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
        df = data_loader('operational_metrics_wide.csv')

        if start_date and end_date:
            # Filter data
            df = df[
                (df['date'] >= pd.to_datetime(start_date)) &
                (df['date'] <= pd.to_datetime(end_date))
            ]
            df['day_of_week'] = df['date'].dt.day_name()

            # Day order for sorting
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            # Figure 1: No-show rate by day of week
            grouped_df = df.groupby('day_of_week', as_index=False)['appointment_no_show_rate'].mean()
            grouped_df['day_of_week'] = pd.Categorical(grouped_df['day_of_week'], categories=day_order, ordered=True)
            grouped_df = grouped_df.sort_values('day_of_week')
            fig1 = px.bar(
                grouped_df,
                x='day_of_week',
                y='appointment_no_show_rate',
                title='Average appointment no-show rate by day of week',
                labels={'day_of_week': 'Day of Week', 'appointment_no_show_rate': 'No-show Rate (%)'}
            )

            # Figure 2: Admissions and discharges by day of week
            grouped_df2 = df.groupby('day_of_week', as_index=False)[['daily_admissions', 'daily_discharges']].mean()
            grouped_df2['day_of_week'] = pd.Categorical(grouped_df2['day_of_week'], categories=day_order, ordered=True)
            grouped_df2 = grouped_df2.sort_values('day_of_week')
            fig2 = px.bar(
                grouped_df2,
                x='day_of_week',
                y=['daily_admissions', 'daily_discharges'],
                barmode='group',
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
                    html.Div(className='kpi-card', children=[html.H4('Admissions'), html.P(f"{df['daily_admissions'].sum()}")]),
                    html.Div(className='kpi-card', children=[html.H4('Discharges'), html.P(f"{df['daily_discharges'].sum()}")]),
                    html.Div(className='kpi-card', children=[html.H4('Bed Occupancy'), html.P(f"{df['bed_occupancy_rate'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card', children=[html.H4('Readmission Rate'), html.P(f"{df['readmission_rate_30d'].mean() / 100:.2%}")]),
                ], className='kpi-row'),

                # Graph Rows
                html.Div([
                    html.Div(dcc.Graph(figure=fig1), className='graph-card'),
                    html.Div(dcc.Graph(figure=fig2), className='graph-card'),
                ], className='graph-row'),

                html.Div([
                    html.Div(dcc.Graph(figure=fig4), className='graph-card'),
                    html.Div(dcc.Graph(figure=fig3), className='graph-card'),
                ], className='graph-row'),
            ])
