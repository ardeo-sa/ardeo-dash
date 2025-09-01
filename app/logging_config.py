"""
Logging configuration module.

Initializes and configures JSON-formatted logging using environment variables:
- LOG_LEVEL: Logging level (default: INFO)
- LOG_FILE: Path to log file (default: app.log)

Intended for use with Promtail/Loki log aggregation.
"""
import logging
from pathlib import Path
from pythonjsonlogger import json

from app import config

def setup_logging():
    """Setup logging handler"""
    log_level = config.LOG_LEVEL
    log_file = Path(config.LOG_FILE)
    # Ensure parent directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    handler = logging.FileHandler(log_file)
    formatter = json.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)
