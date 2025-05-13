"""
Database setup and initialization for the metrics database using SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

from app.config import METRICS_DB_URI

Base = declarative_base()


def get_metrics_engine():
    """
    Creates and returns a SQLAlchemy engine for connecting to the metrics database.

    Raises:
        ValueError: If the METRICS_DB_URI is not defined.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine instance connected to the metrics database.
    Use it when real db is set up
    """
    if not METRICS_DB_URI:
        raise ValueError("The METRICS_DB_URI environment variable is not set or is empty.")
    return create_engine(METRICS_DB_URI, echo=True)


metrics_engine = None
MetricsSessionLocal = None

def init_metrics_db():
    """
    Initializes the metrics database connection by creating the engine and session factory.

    This function sets the global `metrics_engine` and `MetricsSessionLocal` variables.
    Should be called before performing any database operations.

    Raises:
        ValueError: If the METRICS_DB_URI is not defined or the engine could not be initialized.
    """
    global metrics_engine, MetricsSessionLocal
    if not metrics_engine:
        metrics_engine = get_metrics_engine()
        MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)


def get_db() -> Session:
    """
    Provides a database session to be used in FastAPI route functions.

    This will be used as a dependency to inject the session into FastAPI routes.

    Yields:
        Session: A database session instance.
    """
    db = MetricsSessionLocal()
    try:
        yield db
    finally:
        db.close()