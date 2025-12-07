"""add content coulmn to Post Table

Revision ID: 4344fe64d0b5
Revises: fd5990df6fb2
Create Date: 2025-12-06 19:33:21.248712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4344fe64d0b5'
down_revision: Union[str, Sequence[str], None] = 'fd5990df6fb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
