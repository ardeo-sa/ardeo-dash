from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import METRICS_DB_URI


def get_metrics_engine():
    """
    use the above when the database is setup

    """
    return create_engine(METRICS_DB_URI, echo=True)

MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)
Base = declarative_base()
Base.metadata.create_all(bind=metrics_engine)
