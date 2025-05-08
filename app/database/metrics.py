from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import METRICS_DB_URI

Base = declarative_base()

def get_metrics_engine():
    """
    use the above when the database is setup

    """
    return create_engine(METRICS_DB_URI, echo=True)


metrics_engine = None
MetricsSessionLocal = None

def init_metrics_db():
    global metrics_engine, MetricsSessionLocal
    if not metrics_engine:
        metrics_engine = get_metrics_engine()
        MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)

