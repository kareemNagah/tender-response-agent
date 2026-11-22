"""add sha256 to tenders

Revision ID: 7b3e91a4c2d8
Revises: cdac912cd542
Create Date: 2026-11-22 14:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7b3e91a4c2d8"
down_revision: str | Sequence[str] | None = "cdac912cd542"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # NOT NULL with no default: safe only while `tenders` is empty (no write
    # path existed before this column), otherwise existing rows would fail.
    op.add_column("tenders", sa.Column("sha256", sa.String(64), nullable=False))
    op.create_unique_constraint(op.f("uq_tenders_sha256"), "tenders", ["sha256"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_tenders_sha256"), "tenders", type_="unique")
    op.drop_column("tenders", "sha256")
