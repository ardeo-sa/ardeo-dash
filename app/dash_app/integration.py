"""
Module for integrating a Dash dashboard into a FastAPI application using WSGIMiddleware.
"""
from typing import Literal
import logging

from fastapi import FastAPI
from a2wsgi import WSGIMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.config import ARDEO_DATA_SOURCE
from app.dash_app.app import create_dash_app

logger = logging.getLogger(__name__)

DataSource = Literal["synthetic", "real"]


def mount_dash(app: FastAPI, data_source: DataSource | None = None) -> None:
    """
    Mounts a Dash application as a sub-route of a FastAPI app.

    Args:
        app (FastAPI): The FastAPI application to which the Dash app will be mounted.
        data_source: "synthetic" to use CSVs, "real" to use the DB.
    """
    source = data_source or ARDEO_DATA_SOURCE
    if source == "real":
        source_desc = "production DB (real patient metrics)"
    else:
        source_desc = "synthetic CSV files (mock data)"
    logger.info("Mounting Healthcare Dashboard using data source: %s", source_desc)

    logger.info("Mounting Dash app with %s data", data_source)
    try:
        dash_app = create_dash_app(data_source=source)
        app.mount("/dashboard", WSGIMiddleware(dash_app.server))
        logger.info("Dash application mounted at /dashboard")
    except Exception as e:
        logger.exception("Failed to mount Dash application %s", e)
        raise
