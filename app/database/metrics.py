
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import METRICS_DB_URI

metrics_engine = create_engine(METRICS_DB_URI)
MetricsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metrics_engine)
