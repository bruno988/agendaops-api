import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from agendaops.core.cache import delete_cache, get_cache, set_cache
from agendaops.core.deps import get_current_user
from agendaops.db.session import get_db
from agendaops.models.appointment import Appointment
from agendaops.models.idempotency_key import IdempotencyKey
from agendaops.models.user import User
from agendaops.schemas.appointment import AppointmentCreate, AppointmentRead
from agendaops.worker.tasks import send_confirmation_email

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None),
) -> Appointment:
    if idempotency_key:
        existing = db.scalars(
            select(IdempotencyKey).where(IdempotencyKey.key == idempotency_key)
        ).first()
        if existing:
            return AppointmentRead(**json.loads(existing.response_body))

    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    delete_cache("appointments:all")
    send_confirmation_email.delay(
        customer_name=appointment.customer_name,
        service_name=appointment.service_name,
        scheduled_at=appointment.scheduled_at.isoformat(),
    )

    if idempotency_key:
        ikey = IdempotencyKey(
            key=idempotency_key,
            response_body=json.dumps(AppointmentRead.model_validate(appointment).model_dump(mode="json")),
            created_at=datetime.now(timezone.utc),
        )
        db.add(ikey)
        db.commit()

    return appointment


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Appointment]:
    cache_key = "appointments:all"
    cached = get_cache(cache_key)
    if cached:
        logger.info("CACHE HIT — retornando do Redis")
        return cached

    logger.info("CACHE MISS — buscando no PostgreSQL")
    appointments = list(db.scalars(select(Appointment).order_by(Appointment.scheduled_at)).all())
    result = [AppointmentRead.model_validate(a).model_dump(mode="json") for a in appointments]
    set_cache(cache_key, result, ttl=60)
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Appointment:
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment