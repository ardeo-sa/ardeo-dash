"""
This module initializes the SQLAlchemy engine and session for connecting to the primary database.

It creates:
- `primary_engine`: A SQLAlchemy engine for managing the database connection to the primary database.
- `PrimarySessionLocal`: A session factory used to interact with the primary database through SQLAlchemy sessions.

The engine and session are configured based on the database URI defined in the application's settings.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import PRIMARY_DB_URI

primary_engine = create_engine(PRIMARY_DB_URI)
"""
    Creates a SQLAlchemy engine for connecting to the primary database using the 
    PRIMARY_DB_URI from the configuration.

    This engine will be used to manage the connection to the primary database.
"""

PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
"""
    Creates a session factory for the primary database connection using SQLAlchemy's sessionmaker.

    The session is configured with:
        - autocommit=False: Disables automatic commit for the session.
        - autoflush=False: Disables automatic flushing of changes to the database.
        - bind=primary_engine: The session will be bound to the primary database engine.

    The session factory will be used to interact with the primary database.
"""