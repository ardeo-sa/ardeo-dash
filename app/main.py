from fastapi import FastAPI

from app.ModelGenerator import generate_models_to_files
from app.api.routes import metrics
from app.config import PRIMARY_DB_URI
from app.dash_app.integration import mount_dash

app = FastAPI()
app.include_router(metrics.router, prefix="/api")
#generator = generate_models_to_files(PRIMARY_DB_URI)

mount_dash(app)
