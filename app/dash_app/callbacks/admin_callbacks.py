"""
Callbacks for the Admin Metrics

This module defines and registers callbacks responsible for updating the
Admin Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html, dcc
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go
# from utils.data_loader import load_data


def register_admin_callbacks(app, data_loader):
    """
    Register callbacks related to the Admin Metrics tab.

    Args:
        app (dash.Dash): The Dash app instance to register callbacks with.
    """

    @app.callback(
        Output('admin-content', 'children'),
        Input('admin-date-picker-range', 'start_date'),
        Input('admin-date-picker-range', 'end_date')
    )
    def update_admin_metrics(start_date, end_date):
        """
        Update the Admin Metrics content based on the selected date range.

        This callback reads data from 'admin_metrics_wide.csv', filters
        it by the provided date range, and generates KPI cards and multiple
        graphs showing trends and averages.

        Args:
            start_date (str): ISO-format start date string from the DatePickerRange.
            end_date (str): ISO-format end date string from the DatePickerRange.

        Returns:
            html.Div: The updated layout containing KPI cards and Plotly graphs.
        """
        df = data_loader('admin_metrics_wide.csv')

        if start_date and end_date:
            # Filter data
            df = df[
                (df['date'] >= pd.to_datetime(start_date)) &
                (df['date'] <= pd.to_datetime(end_date))
            ]
            df['month'] = df['date'].dt.strftime('%B')
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

            # Figure 1: Metrics Utilisation and Patient to Clinician Ratio
            grouped_df = df.groupby('month', as_index=False)[['imaging_utilization', 'lab_test_utilization', 'treatment_slot_utilization', 'patient_to_clinician_ratio']].mean()
            grouped_df['month'] = pd.Categorical(grouped_df['month'], categories=month_order, ordered=True)
            grouped_df = grouped_df.sort_values('month')
            fig1 = go.Figure()

            fig1.add_trace(go.Bar(
                x=grouped_df['month'],
                y=grouped_df['lab_test_utilization'],
                name='lab test utilisation',
            ))
            fig1.add_trace(go.Bar(
                x=grouped_df['month'],
                y=grouped_df['treatment_slot_utilization'],
                name='treatment slot utilisation',
            ))
            fig1.add_trace(go.Bar(
                x=grouped_df['month'],
                y=grouped_df['imaging_utilization'],
                name='imaging utilisation',
            ))

            fig1.add_trace(go.Scatter(
                x=grouped_df['month'],
                y=grouped_df['patient_to_clinician_ratio'],
                mode='lines+markers',
                name='patient to clinician ratio',
                yaxis='y2',
            ))
            fig1.update_layout(
                barmode='group',
                title='Metrics Utilisation and patient-to-clinician ratio',
                xaxis_title='Month',
                yaxis_title='Utilisation (%)',
                yaxis2=dict(
                    title='Patient-to-Clinician Ratio',
                    overlaying='y',
                    side='right',
                )
            )

            # KPI Cards + Graphs
            return html.Div([
                # KPI Row
                html.Div([
                    html.Div(className='kpi-card',
                             children=[html.H4('Imaging utilisation'), html.P(f"{df['imaging_utilization'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card',
                             children=[html.H4('Lab test utilisation'), html.P(f"{df['lab_test_utilization'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card',
                             children=[html.H4('Treatment slot utilisation'), html.P(f"{df['treatment_slot_utilization'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card',
                             children=[html.H4('Patient to clinician ratio'), html.P(f"{df['patient_to_clinician_ratio'].mean() / 100:.2%}")]),
                ], className='kpi-row'),

                # Graph Rows
                html.Div([
                    html.Div(dcc.Graph(figure=fig1), className='graph-card'),
                ], className='graph-row'),
                ])
