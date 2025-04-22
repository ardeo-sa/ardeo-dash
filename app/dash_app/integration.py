
from fastapi import FastAPI
from dash import Dash
import dash_html_components as html
from starlette.middleware.wsgi import WSGIMiddleware
from .dashboard import create_dashboard

def mount_dash(app: FastAPI):
    dash_app = Dash(__name__, server=False)
    dash_app.layout = create_dashboard()
    app.mount("/dashboard", WSGIMiddleware(dash_app.server))
