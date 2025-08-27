"""
Utility functions for loading and preparing data.

Provides helper functions for loading CSV data files used in the dashboard.
"""

import pandas as pd

def load_data(file_path):
    """
    Load a CSV file into a pandas DataFrame, parsing the 'date' column.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing parsed data.
    """
    return pd.read_csv(file_path, parse_dates=['date'])
