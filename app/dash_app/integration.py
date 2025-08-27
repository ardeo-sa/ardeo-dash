"""
Module for integrating a Dash dashboard into a FastAPI application using WSGIMiddleware.
"""
import logging
from fastapi import FastAPI
from a2wsgi import WSGIMiddleware

from sqlalchemy.exc import SQLAlchemyError

from app.dash_app.dashboard import create_dashboard
from app.dash_app.app import create_dash_app

logger = logging.getLogger(__name__)


def mount_dash(app: FastAPI, data_source: str = "synthetic"):
    """
    Mounts a Dash application as a sub-route of a FastAPI app.

    Args:
        app (FastAPI): The FastAPI application to which the Dash app will be mounted.
    """
    logger.info("Mounting Dash app with %s data", data_source)
    try:
        dash_app = create_dash_app(data_source)
        app.mount("/dashboard", WSGIMiddleware(dash_app.server))
        logger.info("Dash application mounted at /dashboard")
    except SQLAlchemyError as e:
        logger.exception("Failed to mount Dash application %s", e)
