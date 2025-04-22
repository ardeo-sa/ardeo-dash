
import os
from dotenv import load_dotenv

load_dotenv()

PRIMARY_DB_URI = os.getenv("PRIMARY_DB_URI", "sqlite:///primary.db")
METRICS_DB_URI = os.getenv("METRICS_DB_URI", "sqlite:///metrics.db")
