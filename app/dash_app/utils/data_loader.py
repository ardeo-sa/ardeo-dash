"""
Utility functions for loading and preparing data.

Provides helper functions for loading CSV data files used in the dashboard.
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent  # points to app/dash_app

def load_data(file_name):
    """
    Load a CSV file into a pandas DataFrame, parsing the 'date' column.

    Args:
        file_name (str): Name of the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing parsed data.
    """
    file_path = BASE_DIR / "data" / file_name
    return pd.read_csv(file_path, parse_dates=['date'])
