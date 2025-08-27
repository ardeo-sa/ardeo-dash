"""
Callbacks for the Referral Metrics

This module defines and registers callbacks responsible for updating the
Referral Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html, dcc
import pandas as pd
import plotly.express as px
# from utils.data_loader import load_data


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
        df = data_loader('referral_metrics_wide.csv')

        if start_date and end_date:
            # Filter data
            df = df[
                (df['date'] >= pd.to_datetime(start_date)) &
                (df['date'] <= pd.to_datetime(end_date))
            ]
            df['month'] = df['date'].dt.strftime('%B')
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

            # Figure 1: Referral Volume and Referral Conversion Rate
            grouped_df = df.groupby('month', as_index=False)[['referral_volume_daily', 'referral_conversion_rate']].mean()
            grouped_df['month'] = pd.Categorical(grouped_df['month'], categories=month_order, ordered=True)
            grouped_df = grouped_df.sort_values('month')
            fig1 = px.bar(
                grouped_df,
                x='month',
                y=['referral_volume_daily', 'referral_conversion_rate'],
                barmode='group',
                title='Referral volume and referral conversion rate',
                labels={'value': 'Rate (%)', 'month': 'Month', 'variable': 'Metric'}
            )

            # KPI cards + Graphs
            return html.Div([
                # KPI Row
                html.Div([
                    html.Div(className='kpi-card', children=[html.H4('Avg referral to admission time (days)'), html.P(f"{df['referral_to_admission_time'].mean():.2f}")]),
                    html.Div(className='kpi-card', children=[html.H4('Referral volume'), html.P(f"{df['referral_volume_daily'].sum()}")]),
                    html.Div(className='kpi-card', children=[html.H4('Referral source'), html.P(f"{df['referral_source_count'].sum()}")]),
                ], className='kpi-row'),

                # Graph Rows
                html.Div([
                    html.Div(dcc.Graph(figure=fig1), className='graph-card'),
                ], className='graph-row'),
            ])
