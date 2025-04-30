import os

from dotenv import load_dotenv

load_dotenv()

primary_db_user = os.getenv("PRIMARY_DB_USER")
primary_db_password = os.getenv("PRIMARY_DB_PASSWORD")
primary_db_host = os.getenv("PRIMARY_DB_HOST")
primary_db_name = os.getenv("PRIMARY_DB_NAME")

metrics_db_user = os.getenv("METRICS_DB_USER")
metrics_db_password = os.getenv("METRICS_DB_PASSWORD")
metrics_db_host = os.getenv("METRICS_DB_HOST")
metrics_db_name = os.getenv("METRICS_DB_NAME")
metrics_db_port = os.getenv("METRICS_DB_PORT")

PRIMARY_DB_URI = f"mysql+pymysql://{primary_db_user}:{primary_db_password}@{primary_db_host}/{primary_db_name}"
METRICS_DB_URI = f"postgresql://{metrics_db_user}:{metrics_db_password}@{metrics_db_host}:{metrics_db_port}/{metrics_db_name}"
