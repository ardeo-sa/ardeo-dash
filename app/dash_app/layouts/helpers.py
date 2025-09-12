"""
Date picker helper for Dash layouts.

This module provides a utility function `date_picker_container` that
generates a standardized Dash `DatePickerRange` component inside a
container div. The date range is automatically set based on the
`'date'` column of a provided pandas DataFrame.

Usage:
    from app.dash_app.layouts.helpers import date_picker_container
    container = date_picker_container(df, picker_id='my-date-picker')
"""

from dash import html, dcc
import pandas as pd

def date_picker_container(df: pd.DataFrame, picker_id: str) -> html.Div:
    """
    Returns a Div containing a DatePickerRange with min/max/start/end dates
    based on the provided dataframe.

    Args:
        df (pd.DataFrame): DataFrame with a 'date' column.
        picker_id (str): The `id` to assign to the DatePickerRange.

    Returns:
        html.Div: Container div with DatePickerRange inside.
    """
    return html.Div([
        dcc.DatePickerRange(
            id=picker_id,
            min_date_allowed=df['date'].min(),
            max_date_allowed=df['date'].max(),
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD',
            className='date-picker'
        ),
    ], className='date-picker-container')
