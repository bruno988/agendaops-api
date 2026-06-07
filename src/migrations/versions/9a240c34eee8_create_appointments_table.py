"""create appointments table

Revision ID: 9a240c34eee8
Revises: 
Create Date: 2026-06-06 23:29:35.956628

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '9a240c34eee8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("customer_name", sa.String(120), nullable=False),
        sa.Column("professional_name", sa.String(120), nullable=False),
        sa.Column("service_name", sa.String(120), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.Enum("scheduled", "confirmed", "canceled", name="appointmentstatus"), nullable=False, server_default="scheduled"),
        sa.Column("notes", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("appointments")