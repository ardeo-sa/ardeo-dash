"""
This module sets up the FastAPI application and integrates with Dash.

The FastAPI app serves as the backend for API endpoints and is configured
to handle routes related to metrics. It also integrates a Dash app for
visualizing data on a separate `/dashboard` route.

Key Components:
- FastAPI: The main web framework that serves the API endpoints.
- Dash: A framework for building interactive web applications, integrated
  into the FastAPI app.
- Metrics Router: Provides API endpoints related to metrics (via `metrics.router`).
- Mounting Dash: The Dash app is mounted to the `/dashboard` route.

Usage:
    - The FastAPI app will expose API endpoints under the `/api` prefix,
      with routes defined in the `metrics` module.
    - The Dash app is accessible through the `/dashboard` URL, which
      displays metrics in a visual format.

Note:
    - Ensure that the necessary configuration for both FastAPI and Dash
      are set up correctly, including database connections and any Dash
      component dependencies.
"""
from fastapi import FastAPI

from app.api.routes import metrics
from app.dash_app.integration import mount_dash
from app.api.routes import messaging
from app.services.operations.aggregator import processDate

app = FastAPI()
app.include_router(metrics.router, prefix="/api")
app.include_router(messaging.router, prefix="/api")

processDate()
mount_dash(app)
