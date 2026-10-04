"""create tenders table

Revision ID: cdac912cd542
Revises: 
Create Date: 2026-10-04 11:48:01.680417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdac912cd542'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "tenders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(100), nullable=False, server_default="uploaded"),
        sa.Column("storage_key", sa.String(512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tenders")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tenders")
