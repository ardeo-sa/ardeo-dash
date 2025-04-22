
from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0"
)

celery.conf.update(
    task_track_started=True,
    task_time_limit=30 * 60,
)
