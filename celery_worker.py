import os
from celery import Celery

def make_celery():
    broker = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    backend = broker
    celery = Celery(__name__, broker=broker, backend=backend)
    celery.conf.task_routes = {"app.tasks.*": {"queue": "default"}}
    return celery

celery = make_celery()
