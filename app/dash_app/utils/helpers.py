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


DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTH_ORDER = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

def _grouped_chart(df, group_col, columns, order=None, title="", labels=None, barmode='group'):
    """
    Generic helper to create a grouped chart by a categorical column (day or month).

    Args:
        df (pd.DataFrame): DataFrame with data.
        group_col (str): Column to group by.
        columns (list[str]): Columns to aggregate and plot.
        order (list[str], optional): Categorical order for sorting.
        title (str, optional): Title of the chart.
        labels (dict, optional): Labels for Plotly chart.
        barmode (str, optional): Barmode for bar charts (ignored for line charts).

    Returns:
        plotly.express.Figure: The resulting chart.
    """
    grouped_df = df.groupby(group_col, as_index=False)[columns].mean()
    if order:
        grouped_df[group_col] = pd.Categorical(grouped_df[group_col], categories=order, ordered=True)
    grouped_df = grouped_df.sort_values(group_col)

    if len(columns) == 1:
        return px.line(grouped_df, x=group_col, y=columns[0], title=title, labels=labels or {group_col: group_col})
    else:
        return px.bar(grouped_df, x=group_col, y=columns, barmode=barmode, title=title,
                      labels=labels or {group_col: group_col})

def grouped_day_bar(df, columns, title, labels=None, barmode='group'):
    """
    Create a grouped bar/line chart by day of week.
    """
    return _grouped_chart(df, 'day_of_week', columns, order=DAY_ORDER, title=title,
                          labels=labels, barmode=barmode)

def grouped_month_bar(df, columns, title="", labels=None, month_order=None):
    """
    Create a grouped bar/line chart by month.
    """
    return _grouped_chart(df, 'month', columns, order=month_order or MONTH_ORDER, title=title, labels=labels)

def load_and_filter(data_loader, filename, start_date, end_date, add_day=False, add_month=False):
    """
    Load a CSV via data_loader, filter by date range, and optionally add day/month columns.

    Args:
        data_loader (Callable): Function to load CSV by filename.
        filename (str): File to load.
        start_date (str | datetime): Inclusive start date.
        end_date (str | datetime): Inclusive end date.
        add_day (bool): Whether to add 'day_of_week' column.
        add_month (bool): Whether to add 'month' column.

    Returns:
        pd.DataFrame | None: Filtered DataFrame, or None if dates are missing.
    """
    if not (start_date and end_date):
        return None

    df = data_loader(filename)
    df = df[
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]

    if add_day:
        df['day_of_week'] = df['date'].dt.day_name()
    if add_month:
        df['month'] = df['date'].dt.strftime('%B')

    return df
