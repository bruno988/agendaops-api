from celery import Celery

from agendaops.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "agendaops",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["agendaops.worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Sao_Paulo",
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    broker_connection_retry_on_startup=True,
)