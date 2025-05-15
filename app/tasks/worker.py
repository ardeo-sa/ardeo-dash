"""
This module sets up the Celery configuration for task execution.

It initializes a Celery instance with Redis as the message broker and
configures task settings such as tracking task progress and setting a
time limit for task execution.

The configuration is crucial for managing asynchronous task execution
within the application.

Configuration:
    - `broker`: Defines the message broker used by Celery, in this case, Redis.
    - `task_track_started`: Ensures that Celery tracks the state of tasks once they are started.
    - `task_time_limit`: Sets a time limit of 30 minutes (1800 seconds) for task execution.

Usage:
    To use this Celery configuration, import the `celery` instance into
    other modules and define tasks that will be executed asynchronously.

Note:
    Ensure that Redis is installed and running at the specified address
    (`redis://localhost:6379/0`), or update the broker URL accordingly.
"""
from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0"
)

celery.conf.update(
    task_track_started=True,
    task_time_limit=30 * 60,
)
