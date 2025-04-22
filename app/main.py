
from fastapi import FastAPI
from app.api.routes import metrics
from app.dash_app.integration import mount_dash

app = FastAPI()
app.include_router(metrics.router, prefix="/api")

mount_dash(app)
