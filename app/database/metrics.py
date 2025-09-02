"""
Database setup and initialization for the metrics database using SQLAlchemy.
"""
# pylint: disable=invalid-name
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import OperationalError

from app.config import METRICS_DB_URI, METRICS_DB_URI_READ, BOOTSTRAP_METRICS_DB

metadata = MetaData(schema="reporting")
Base = declarative_base(metadata=metadata)

global metrics_engine, MetricsSessionLocal, metrics_read_engine, MetricsReadSessionLocal



def init_metrics_engine():
    """
    Initializes the metrics database connection by creating the engine and session factory.

    This function sets the global `metrics_engine` and `MetricsSessionLocal` variables.
    Should be called before performing any database operations.

    Raises:
        ValueError: If the METRICS_DB_URI is not defined or the engine could not be initialized.
    """
    global metrics_engine, MetricsSessionLocal # pylint: disable=global-statement
    if not METRICS_DB_URI:
        raise ValueError("METRICS_DB_URI is not set.")

    # Full-access engine and session
    metrics_engine = create_engine(METRICS_DB_URI, echo=True, future=True)
    MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)

    # Read-only engine and session
    metrics_read_engine = create_engine(METRICS_DB_URI_READ, echo=False, future=True)
    MetricsReadSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_read_engine)

    if BOOTSTRAP_METRICS_DB:
        print("BOOTSTRAP_METRICS_DB is enabled — skipping connection test and creating tables.")
        Base.metadata.create_all(bind=metrics_engine)
    else:
        try:
            with metrics_engine.connect() as _:
                pass  # Test connection
        except OperationalError as e:
            raise RuntimeError(f"Error: Cannot connect to metrics database: {e}") from e

def get_db() -> Session:
    """
    Provides a database session to be used in FastAPI route functions.

    This will be used as a dependency to inject the session into FastAPI routes.

    Yields:
        Session: A database session instance.
    """
    if not MetricsSessionLocal:
        raise RuntimeError("Metrics DB session is not available.")

    db = MetricsSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_metrics_engine(echo=False):
    """
    Returns a SQLAlchemy engine for the metrics database.

    Args:
        echo (bool): Enable SQL echoing for debugging.

    Returns:
        sqlalchemy.engine.Engine
    """
    if not METRICS_DB_URI:
        raise ValueError("METRICS_DB_URI is not set.")
    return create_engine(METRICS_DB_URI, echo=echo)
