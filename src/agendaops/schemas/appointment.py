from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from agendaops.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    professional_name: str = Field(min_length=2, max_length=120)
    service_name: str = Field(min_length=2, max_length=120)
    scheduled_at: datetime
    notes: str | None = Field(default=None, max_length=1000)


class AppointmentRead(BaseModel):
    id: int
    customer_name: str
    professional_name: str
    service_name: str
    scheduled_at: datetime
    status: AppointmentStatus
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)
    duration_minutes: int | None = None
