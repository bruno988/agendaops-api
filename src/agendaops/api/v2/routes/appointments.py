from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from agendaops.core.deps import get_current_user
from agendaops.db.session import get_db
from agendaops.models.appointment import Appointment
from agendaops.models.user import User

router = APIRouter(prefix="/appointments", tags=["appointments-v2"])


@router.get("")
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    appointments = db.scalars(select(Appointment).order_by(Appointment.scheduled_at)).all()
    return {
        "version": "v2",
        "total": len(list(appointments)),
        "requested_by": current_user.username,
        "data": [
            {
                "id": a.id,
                "customer": a.customer_name,
                "professional": a.professional_name,
                "service": a.service_name,
                "scheduled_at": a.scheduled_at.isoformat(),
                "status": a.status,
            }
            for a in appointments
        ],
    }