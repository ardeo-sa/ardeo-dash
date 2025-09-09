"""
This module initializes the SQLAlchemy engine and session for connecting to the primary database.

It creates:
- `PRIMARY_ENGINE`: A SQLAlchemy engine for managing the database connection to the primary database using the
    PRIMARY_DB_URI from the configuration.
- `PrimarySessionLocal`: A session factory used to interact with the primary database through SQLAlchemy sessions.
    The session is configured with:
        - autocommit=False: Disables automatic commit for the session.
        - autoflush=False: Disables automatic flushing of changes to the database.
        - bind=PRIMARY_ENGINE: The session will be bound to the primary database engine.

The engine and session are configured based on the database URI defined in the application's settings.
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.config import PRIMARY_DB_URI, DISABLE_PRIMARY_DB

logger = logging.getLogger(__name__)

PRIMARY_ENGINE = None
PRIMARY_SESSION_LOCAL = None

def init_primary_engine():
    """
    Initializes the primary database engine and session factory if not disabled.
    """
    global PRIMARY_ENGINE, PRIMARY_SESSION_LOCAL  # pylint: disable=global-statement

    if DISABLE_PRIMARY_DB:
        logger.info("Primary DB engine creation skipped due to DISABLE_PRIMARY_DB flag.")
        return

    try:
        PRIMARY_ENGINE = create_engine(PRIMARY_DB_URI)
        with PRIMARY_ENGINE.connect() as _:
            logger.info("Successfully connected to primary database.")
        PRIMARY_SESSION_LOCAL = sessionmaker(
            autocommit=False, autoflush=False, bind=PRIMARY_ENGINE
        )
    except SQLAlchemyError as e:
        logger.warning("Failed to create primary DB engine/session: %s", e)
        PRIMARY_ENGINE = None
        PRIMARY_SESSION_LOCAL = None
