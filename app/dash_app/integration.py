
from dash import Dash
from starlette.middleware.wsgi import WSGIMiddleware
from app.dash_app.dashboard import create_dashboard

def mount_dash(app: FastAPI):
    dash_app = Dash(__name__, server=False)
    dash_app.layout = create_dashboard()
    app.mount("/dashboard", WSGIMiddleware(dash_app.server))
