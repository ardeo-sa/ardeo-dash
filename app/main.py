
from fastapi import FastAPI
from app.api.routes import metrics
from app.dash_app.integration import mount_dash
from app.api.routes import messaging

app = FastAPI()
app.include_router(metrics.router, prefix="/api")
app.include_router(messaging.router, prefix="/api")

mount_dash(app)
