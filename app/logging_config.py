"""
Logging configuration module.

Initializes and configures JSON-formatted logging using environment variables:
- LOG_LEVEL: Logging level (default: INFO)
- LOG_FILE: Path to log file (default: app.log)

Intended for use with Promtail/Loki log aggregation.
"""

import os
import logging
from pythonjsonlogger import json

def setup_logging():
    """Setup logging handler"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "app.log")

    logger = logging.getLogger()
    logger.setLevel(log_level)

    handler = logging.FileHandler(log_file)
    formatter = json.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)
