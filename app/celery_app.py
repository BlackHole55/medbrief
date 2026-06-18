import os
from celery import Celery

from app.config import settings

REDIS_BROKER_URL = settings.CELERY_BROKER_URL
REDIS_BACKEND_URL = settings.CELERY_BACKEND_URL

celery_app = Celery(
    "medbrief",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BACKEND_URL,
)

celery_app.conf.update(
    imports=("app.workers",),
    task_track_started=True,

    # Enforce JSON for security and language interoperability. 
    # Avoid pickle unless you absolutely need to pass complex Python objects.
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    timezone="UTC",
    enable_utc=True,

    # Store results for 24 hours (86400 seconds) to prevent Redis memory bloat
    result_expires=86400,
    # If a task fails, keep the traceback information in the backend
    result_extended=True,

    task_acks_late=True,

    # Prefetch multiplier dictates how many tasks a worker process pulls at once.
    # A value of 1 prevents a worker from "hoarding" long-running AI/Summary tasks 
    # while other workers sit idle.
    worker_prefetch_multiplier=1,

    task_annotations={
        "*": {
            "autoretry_for": (Exception,),      # Catch all unhandled exceptions
            "max_retries": 3,                   # Retry up to 3 times before failing
            "default_retry_delay": 180,         # Wait 3 minutes before retrying
            "retry_backoff": True,              # Exponential backoff (e.g., 2s, 4s, 8s...)
            "retry_backoff_max": 600,           # Caps exponential delay at 10 minutes
            "retry_jitter": True,               # Add random noise to delay to avoid thundering herd
        }
    },
)