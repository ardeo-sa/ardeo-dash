"""
This module sets up the FastAPI application and integrates with Dash.

The FastAPI app serves as the backend for API endpoints and is configured
to handle routes related to metrics. It also integrates a Dash app for
visualizing data on a separate `/dashboard` route.

Key Components:
- FastAPI: The main web framework that serves the API endpoints.
- Dash: A framework for building interactive web applications, integratedcinto the FastAPI app.
- Metrics Router: Provides API endpoints related to metrics (via `metrics.router`).
- Mounting Dash: The Dash app is mounted to the `/dashboard` route.

Usage:
    - The FastAPI app will expose API endpoints under the `/api` prefix with routes defined in the `metrics` module.
    - The Dash app is accessible through the `/dashboard` URL, which displays metrics in a visual format.

Note:
    - Ensure that the necessary configuration for both FastAPI and Dash are set up correctly,
    including database connections and any Dash component dependencies.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import metrics
from app.dash_app.integration import mount_dash
from app.services.data_importers.port_primary_data import port_primary_data
from app.services.data_processing.process_primary_data import process_data
from app.database.metrics import init_metrics_engine
from app.database.primary import init_primary_engine
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.

    Handles startup and shutdown tasks:
        - Startup:
            1. Initializes the primary database engine.
            2. Initializes the metrics database engine.
            3. Imports and ports primary data.
            4. Processes primary data.
            5. Mounts the Dash application to `/dashboard`.
        - Shutdown: No explicit tasks defined (placeholder).
    """
    try:
        init_primary_engine()
        init_metrics_engine()
        port_primary_data()
        process_data()
        mount_dash(app)
        logger.info("Startup completed successfully.")
    except (SQLAlchemyError, RuntimeError) as e:
        logger.error("Startup failure: %s", e, exc_info=True)
    yield
    # Optional: add cleanup/shutdown logic here if needed
    logger.info("Shutdown complete.")


app = FastAPI()
app.include_router(metrics.router, prefix="/api")


@app.get("/health")
def health():
    """
    Health check endpoint.

    Returns a simple JSON response indicating that the API is running.

    Returns:
        dict: A dictionary with a single key 'status' set to 'ok'.
    """
    logger.info("Health endpoint called")
    return {"status": "ok"}


# Instrumentation for Prometheus monitoring
Instrumentator().instrument(app).expose(app)
