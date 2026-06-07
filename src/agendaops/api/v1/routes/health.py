import time
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from agendaops.core.config import get_settings
from agendaops.db.session import get_db
from agendaops.models.appointment import Appointment
from sqlalchemy.orm import Session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@router.get("/slow")
def slow_health_check() -> dict[str, str]:
    time.sleep(35)
    return {"status": "slow-ok"}


@router.get("/transaction-test")
def transaction_test(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        a = Appointment(
            customer_name="Teste",
            professional_name="Dr. Teste",
            service_name="Teste",
            scheduled_at=datetime.now(timezone.utc),
        )
        db.add(a)
        raise Exception("Erro simulado antes do commit!")
        db.commit()
    except Exception as e:
        db.rollback()
        return {"status": "rollback feito", "erro": str(e)}