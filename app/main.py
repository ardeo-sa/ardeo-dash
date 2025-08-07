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
import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import metrics
from app.dash_app.integration import mount_dash
from app.services.process_data.port_primary_data import portprimarydata
from app.services.operations.aggregator import process_data
from app.database.metrics import init_metrics_engine
from app.database.primary import init_primary_engine
from app.logging_config import setup_logging

setup_logging()
app = FastAPI()
app.include_router(metrics.router, prefix="/api")

logger = logging.getLogger(__name__)

@app.on_event("startup")
def on_startup():
    try:
        init_primary_engine()
        init_metrics_engine()
        portprimarydata()
        process_data()
        mount_dash(app)
    except Exception as e:
        logger.error(f"Startup failure: {e}", exc_info=True)

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    """Endpoint to check app health status"""
    logger.info("Health endpoint called")
    return {"status": "ok"}
