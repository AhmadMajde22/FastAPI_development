"""add the rest Fileds for the posts table

Revision ID: 6d12e08a7953
Revises: 45bee43a5992
Create Date: 2025-12-06 20:55:08.635277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d12e08a7953'
down_revision: Union[str, Sequence[str], None] = '45bee43a5992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="TRUE"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")))


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
