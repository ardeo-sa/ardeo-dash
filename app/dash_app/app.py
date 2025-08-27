"""
Main entry point for the Ardeo Dashboard Plotly Dash app.

This version is refactored for integration with FastAPI.
Instead of always running standalone, we expose `create_dash_app()`
so it can be mounted inside FastAPI, with a switch for real/synthetic data.
"""

from dash import Dash
from app.dash_app.layout import create_layout
from app.dash_app.callbacks import register_callbacks
from app.dash_app.data_sources import get_data_loader


def create_dash_app(data_source: str = "synthetic") -> Dash:
    """
    Factory function to create and configure a Dash app.

    Args:
        data_source: "real" (database) or "synthetic" (sample CSV data).
    """
    dash_app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        requests_pathname_prefix="/dashboard/",
        assets_url_path="/dashboard/assets"
    )
    dash_app.title = "Healthcare Dashboard"

    data_loader = get_data_loader(data_source)

    dash_app.layout = create_layout()
    register_callbacks(dash_app, data_loader)

    return dash_app


# Allow running standalone for development
if __name__ == "__main__":
    app = create_dash_app("synthetic")
    app.run(debug=True)
