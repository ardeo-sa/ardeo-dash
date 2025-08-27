"""
Callbacks for the Pathway Metrics

This module defines and registers callbacks responsible for updating the
Pathway Metrics tab content, including KPI cards and graphs, based on
user-selected date ranges.
"""

from dash import Output, Input, html, dcc
import pandas as pd
import plotly.express as px
# from utils.data_loader import load_data


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
        df = data_loader('app/dash_app/data/pathway_metrics_wide.csv')

        if start_date and end_date:
            # Filter data
            df = df[
                (df['date'] >= pd.to_datetime(start_date)) &
                (df['date'] <= pd.to_datetime(end_date))
            ]

            # Month column for grouping
            df['month'] = df['date'].dt.strftime('%B')
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

            # Figure 1: Dropout vs adherence rates by month
            grouped_df = df.groupby('month', as_index=False)[['pathway_adherence_rate', 'pathway_dropout_rate']].mean()
            grouped_df['month'] = pd.Categorical(grouped_df['month'], categories=month_order, ordered=True)
            grouped_df = grouped_df.sort_values('month')
            fig1 = px.bar(
                grouped_df,
                x='month',
                y=['pathway_adherence_rate', 'pathway_dropout_rate'],
                barmode='group',
                title='Avg dropout and adherence rate',
                labels={'value': 'Rate (%)', 'month': 'Month', 'variable': 'Metric'}
            )

            # Figure 2: Treatment duration over time
            fig2 = px.line(
                df,
                x='date',
                y='pathway_treatment_duration',
                title='Avg treatment duration',
                labels={'treatment_duration_days': 'Days', 'date': 'Date'}
            )

            # Figure 3: Relapse vs readmission rates by month
            grouped_df2 = df.groupby('month', as_index=False)[['pathway_relapse_rate', 'pathway_readmission_rate']].mean()
            grouped_df2['month'] = pd.Categorical(grouped_df['month'], categories=month_order, ordered=True)
            grouped_df2 = grouped_df2.sort_values('month')
            fig3 = px.bar(
                grouped_df2,
                x='month',
                y=['pathway_relapse_rate', 'pathway_readmission_rate'],
                barmode='group',
                title='Avg relapse and readmission rate',
                labels={'value': 'Rate (%)', 'month': 'Month', 'variable': 'Metric'}
            )

            # KPI cards + Graphs
            return html.Div([
                # KPI Row
                html.Div([
                    html.Div(className='kpi-card', children=[html.H4('Success rate'), html.P(f"{df['pathway_success_rate'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card', children=[html.H4('Failure rate'), html.P(f"{df['pathway_failure_rate'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card', children=[html.H4('Complication rate'), html.P(f"{df['pathway_complication_rate'].mean() / 100:.2%}")]),
                    html.Div(className='kpi-card', children=[html.H4('Adherence rate'), html.P(f"{df['pathway_adherence_rate'].mean() / 100:.2%}")]),
                ], className='kpi-row'),

                # Graph Row
                html.Div([
                    html.Div(dcc.Graph(figure=fig1), className='graph-card'),
                    html.Div(dcc.Graph(figure=fig2), className='graph-card'),
                ], className='graph-row'),

                html.Div([
                    html.Div(dcc.Graph(figure=fig3), className='graph-card'),
                ], className='graph-row'),
            ])
