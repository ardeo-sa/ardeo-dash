"""
This module initializes the SQLAlchemy engine and session for connecting to the primary database.

It creates:
- `primary_engine`: A SQLAlchemy engine for managing the database connection to the primary database using the
    PRIMARY_DB_URI from the configuration.
- `PrimarySessionLocal`: A session factory used to interact with the primary database through SQLAlchemy sessions.
    The session is configured with:
        - autocommit=False: Disables automatic commit for the session.
        - autoflush=False: Disables automatic flushing of changes to the database.
        - bind=primary_engine: The session will be bound to the primary database engine.

The engine and session are configured based on the database URI defined in the application's settings.
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import PRIMARY_DB_URI, DISABLE_PRIMARY_DB

logger = logging.getLogger(__name__)

primary_engine = None
PrimarySessionLocal = None

def init_primary_engine():
    """
    Initializes the primary database engine and session factory if not disabled.
    """
    global primary_engine, PrimarySessionLocal  # pylint: disable=global-statement

    if DISABLE_PRIMARY_DB:
        logger.info("Primary DB engine creation skipped due to DISABLE_PRIMARY_DB flag.")
        return

    try:
        primary_engine = create_engine(PRIMARY_DB_URI)
        with primary_engine.connect() as conn:
            logger.info("Successfully connected to primary database.")
        PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
    except Exception as e:
        logger.warning(f"Failed to create primary DB engine/session: {e}")
        primary_engine = None
        PrimarySessionLocal = None
