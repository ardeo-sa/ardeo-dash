# pylint: disable=R0801
"""
Callbacks for the MDT Metrics

This module defines and registers callbacks responsible for updating the
MDT Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go
# from utils.data_loader import load_data
from app.dash_app.utils.helpers import build_graph_rows, grouped_month_bar, load_and_filter


def register_mdt_callbacks(app, data_loader):
    """
    Register callbacks related to the MDT Metrics tab.

    Args:
        app (dash.Dash): The Dash app instance to register callbacks with.
    """

    @app.callback(
        Output('mdt-content', 'children'),
        Input('mdt-date-picker-range', 'start_date'),
        Input('mdt-date-picker-range', 'end_date')
    )
    def update_mdt_metrics(start_date, end_date):
        """
        Update the MDT Metrics content based on the selected date range.

        This callback reads data from 'mdt_metrics_wide.csv', filters
        it by the provided date range, and generates KPI cards and multiple
        graphs showing trends and averages.

        Args:
            start_date (str): ISO-format start date string from the DatePickerRange.
            end_date (str): ISO-format end date string from the DatePickerRange.

        Returns:
            html.Div: The updated layout containing KPI cards and Plotly graphs.
        """
        # Return empty if dates are missing
        df = load_and_filter(
            data_loader,
            'mdt_metrics_wide.csv',
            start_date,
            end_date,
            add_day=True,
            add_month=True
        )
        if df is None:
            return html.Div()

        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

        # Figure 1: MDT Completion rate and MDT Average Attendance
        fig1 = grouped_month_bar(
            df,
            columns=['mdt_action_completion_rate', 'mdt_avg_attendance'],
            month_order=month_order,
            title='MDT Completion rate and MDT Average Attendance',
            labels={'month': 'Month', 'mdt_action_completion_rate': 'MDT Completion Rate',
                    'mdt_avg_attendance': 'MDT Average Attendance'}
        )

        # Figure 2: MDT Meeting Time and Case Discussion Time
        grouped_df2 = df.groupby('month', as_index=False)[['mdt_avg_case_discussion_time',
                                                           'mdt_meeting_count']].mean()
        grouped_df2['month'] = pd.Categorical(grouped_df2['month'], categories=month_order, ordered=True)
        grouped_df2 = grouped_df2.sort_values('month')
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=grouped_df2['month'],
            y=grouped_df2['mdt_meeting_count'],
            name='MDT meeting count',
        ))
        fig2.add_trace(go.Scatter(
            x=grouped_df2['month'],
            y=grouped_df2['mdt_avg_case_discussion_time'],
            mode='lines+markers',
            name='MDT avg case discussion time',
            yaxis='y2',
        ))
        fig2.update_layout(
            barmode='group',
            title='MDT meeting time and case discussion time',
            xaxis_title='Month',
            yaxis_title='MDT meeting count',
            yaxis2={
                "title": "MDT avg case discussion time",
                "overlaying": "y",
                "side": "right",
            }
        )

        # KPI cards + Graphs
        return html.Div([
            html.Div([
                html.Div(className='kpi-card', children=[html.H4('MDT meeting count'),
                                                         html.P(f"{df['mdt_meeting_count'].sum():.0f}")]),
                html.Div(className='kpi-card', children=[html.H4('MDT average wait time (days)'),
                                                         html.P(f"{df['mdt_avg_wait_time'].mean():.2f}")]),
                html.Div(className='kpi-card', children=[html.H4('MDT completion rate'),
                                                         html.P(
                                                             f"{df['mdt_action_completion_rate'].mean() / 100:.2%}")]),
            ], className='kpi-row'),

            *build_graph_rows(fig1, fig2)
        ])
