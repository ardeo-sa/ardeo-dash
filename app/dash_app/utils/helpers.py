"""
Helper functions for building Dash layouts and Plotly visualizations.

This module provides reusable utilities for:

- Creating consistent Dash HTML blocks for multiple graphs (`build_graph_rows`).
- Filtering pandas DataFrames by a date range (`filter_by_date`).
- Generating grouped bar charts by month (`grouped_month_bar`).

These helpers are designed to reduce duplication and standardize
layout and visualization patterns across the Ardeo Healthcare Dashboard.
"""

import pandas as pd
import plotly.express as px
from dash import html, dcc


def build_graph_rows(fig1, fig2=None, fig3=None):
    """
    Build a reusable block of Dash HTML for displaying up to three graphs
    in consistent layout rows.

    Args:
        fig1 (plotly.graph_objects.Figure): The first figure to display.
        fig2 (plotly.graph_objects.Figure, optional): The second figure to display.
        fig3 (plotly.graph_objects.Figure, optional): The third figure to display.

    Returns:
        list[html.Div]: A list of Div elements containing the provided figures.
    """
    rows = [
        html.Div([
            html.Div(dcc.Graph(figure=fig1), className='graph-card'),
            *( [html.Div(dcc.Graph(figure=fig2), className='graph-card')] if fig2 else [] )
        ], className='graph-row')
    ]

    if fig3:
        rows.append(
            html.Div([
                html.Div(dcc.Graph(figure=fig3), className='graph-card'),
            ], className='graph-row')
        )

    return rows


def filter_by_date(df, start_date, end_date):
    """
    Filter a dataframe by a start and end date.

    Args:
        df (pd.DataFrame): The dataframe to filter. Must have a 'date' column.
        start_date (str | datetime): Start date (inclusive).
        end_date (str | datetime): End date (inclusive).

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    if start_date and end_date:
        df = df[
            (df['date'] >= pd.to_datetime(start_date)) &
            (df['date'] <= pd.to_datetime(end_date))
        ]
    return df


def grouped_month_bar(df, columns, month_order=None, title="", labels=None):
    """
    Create a grouped bar chart by month from specified columns.

    Args:
        df (pd.DataFrame): The dataframe with a 'date' column.
        columns (list[str]): Columns to aggregate and plot.
        month_order (list[str], optional): Order of months for sorting.
        title (str, optional): Title of the figure.
        labels (dict, optional): Labels for Plotly.

    Returns:
        plotly.express.Figure: The resulting grouped bar chart.
    """
    df['month'] = df['date'].dt.strftime('%B')
    if month_order is None:
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

    grouped_df = df.groupby('month', as_index=False)[columns].mean()
    grouped_df['month'] = pd.Categorical(grouped_df['month'], categories=month_order, ordered=True)
    grouped_df = grouped_df.sort_values('month')

    fig = px.bar(
        grouped_df,
        x='month',
        y=columns,
        barmode='group',
        title=title,
        labels=labels
    )
    return fig
