import os

from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER", "emdtuser")
db_password = os.getenv("DB_PASSWORD", "6f62da594ee4995ef4fbe526c8a55ada")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "ardeocore")

PRIMARY_DB_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
METRICS_DB_URI = os.getenv("METRICS_DB_URI", "sqlite:///metrics.db")
