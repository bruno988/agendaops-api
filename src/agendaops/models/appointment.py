from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from agendaops.db.base import Base


class AppointmentStatus(StrEnum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    canceled = "canceled"


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        Index("ix_appointments_customer_name", "customer_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    professional_name: Mapped[str] = mapped_column(String(120), nullable=False)
    service_name: Mapped[str] = mapped_column(String(120), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus), default=AppointmentStatus.scheduled, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)