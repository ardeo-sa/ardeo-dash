"""
Module for integrating a Dash dashboard into a FastAPI application using WSGIMiddleware.
"""
import logging
from dash import Dash
from fastapi import FastAPI
from a2wsgi import WSGIMiddleware

from sqlalchemy.exc import SQLAlchemyError

from app.dash_app.dashboard import create_dashboard

logger = logging.getLogger(__name__)


def mount_dash(app: FastAPI):
    """
    Mounts a Dash application as a sub-route of a FastAPI app.

    Args:
        app (FastAPI): The FastAPI application to which the Dash app will be mounted.
    """
    logger.info("Initializing Dash application.")
    try:
        dash_app = Dash(__name__, server=False)
        dash_app.layout = create_dashboard()
        app.mount("/dashboard", WSGIMiddleware(dash_app.server))
        logger.info("Dash application mounted at /dashboard.")
    except SQLAlchemyError as e:
        logger.exception("Failed to mount Dash application %s", e)
