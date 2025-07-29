import os
import logging
from pythonjsonlogger import json

def setup_logging():
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