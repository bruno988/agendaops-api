import logging

from agendaops.worker.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def send_confirmation_email(self, customer_name: str, service_name: str, scheduled_at: str) -> dict:
    try:
        logger.info(f"Enviando email para {customer_name} — {service_name} em {scheduled_at}")
        # aqui entraria o código real de envio de email
        # por enquanto simulamos
        logger.info(f"Email enviado com sucesso para {customer_name}")
        return {"status": "sent", "customer": customer_name}
    except Exception as exc:
        logger.error(f"Erro ao enviar email: {exc}. Tentativa {self.request.retries + 1} de {self.max_retries + 1}")
        raise self.retry(exc=exc)