"""Database configuration module for loading and constructing DB URIs from environment
variables."""

import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

load_dotenv()

primary_db_user = os.getenv("PRIMARY_DB_USER", "user123")
primary_db_password = os.getenv("PRIMARY_DB_PASSWORD", "pass123")
primary_db_host = os.getenv("PRIMARY_DB_HOST", "someurl")
primary_db_name = os.getenv("PRIMARY_DB_NAME", "myprimarydb")

metrics_db_user = os.getenv("METRICS_DB_USER", "user123")
metrics_db_password = os.getenv("METRICS_DB_PASSWORD", "pass123")
metrics_db_host = os.getenv("METRICS_DB_HOST", "someurl")
metrics_db_name = os.getenv("METRICS_DB_NAME", "myreportingdb")
metrics_db_port = os.getenv("METRICS_DB_PORT", "1234")


required_vars = {
    "METRICS_DB_USER": metrics_db_user,
    "METRICS_DB_PASSWORD": metrics_db_password,
    "METRICS_DB_HOST": metrics_db_host,
    "METRICS_DB_PORT": metrics_db_port,
    "METRICS_DB_NAME": metrics_db_name,
}

missing = [key for key, value in required_vars.items() if value is None]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

PRIMARY_DB_URI = (f"mysql+pymysql://{primary_db_user}:{primary_db_password}@{primary_db_host}/"
                  f"{primary_db_name}")
Base = declarative_base()

METRICS_DB_URI = (f"postgresql://{metrics_db_user}:{metrics_db_password}@{metrics_db_host}:"
                  f"{metrics_db_port}/{metrics_db_name}")
