import resend
from celery import Celery
from src.core.pydantic_configuration import config


broker = f"{config.REDIS_URL}/0"
backend= f"{config.REDIS_URL}/1"
celery_app = Celery("shopbebta", backend=backend, broker=broker)

resend.api_key = config.RESEND_API_KEY

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    include=[
        "src.tasks.notification_tasks",
        "src.tasks.email_task"
    ]
)

