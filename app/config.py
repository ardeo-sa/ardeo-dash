"""Database configuration module for loading and constructing DB URIs from environment
variables."""

import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

load_dotenv()

DISABLE_PRIMARY_DB = os.getenv("DISABLE_PRIMARY_DB", "false").lower() == "true"
BOOTSTRAP_METRICS_DB = os.getenv("BOOTSTRAP_METRICS_DB", "false").lower() == "true"

primary_db_user = os.getenv("PRIMARY_DB_USER", "user123")
primary_db_password = os.getenv("PRIMARY_DB_PASSWORD", "pass123")
primary_db_host = os.getenv("PRIMARY_DB_HOST", "someurl")
primary_db_name = os.getenv("PRIMARY_DB_NAME", "myprimarydb")

metrics_db_user = os.getenv("METRICS_DB_USER", "user123")
metrics_db_password = os.getenv("METRICS_DB_PASSWORD", "pass123")
metrics_db_host = os.getenv("METRICS_DB_HOST", "someurl")
metrics_db_name = os.getenv("METRICS_DB_NAME", "myreportingdb")
metrics_db_port = os.getenv("METRICS_DB_PORT", "1234")

# Read-only metrics DB user
metrics_db_read_user = os.getenv("METRICS_DB_READ_USER", "reporting_user")
metrics_db_read_password = os.getenv("METRICS_DB_READ_PASSWORD", "readonlypassword")

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

# Construct read-only DB URI
METRICS_DB_URI_READ = (
    f"postgresql://{metrics_db_read_user}:{metrics_db_read_password}@"
    f"{metrics_db_host}:{metrics_db_port}/{metrics_db_name}"
)


# Settings for data scraping
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TIMEOUT = int(os.getenv("TIMEOUT", "5"))
DISABLE_MEETINGS_FETCH = os.getenv("DISABLE_MEETINGS_FETCH", "false").lower() == "true"

# Dashboard data source toggle
ARDEO_DATA_SOURCE = os.getenv("ARDEO_DATA_SOURCE", "synthetic").lower()
if ARDEO_DATA_SOURCE not in ("synthetic", "real"):
    raise ValueError(
        f"Invalid ARDEO_DATA_SOURCE={ARDEO_DATA_SOURCE}. "
        "Must be 'synthetic' or 'real'."
    )

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# If the env only provides a filename, put it under ./logs
log_file_env = os.getenv("LOG_FILE", "app.log")
if os.path.isabs(log_file_env):
    LOG_FILE = log_file_env
else:
    LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", log_file_env)
    LOG_FILE = os.path.abspath(LOG_FILE)
