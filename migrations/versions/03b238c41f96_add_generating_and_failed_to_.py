"""add generating and failed  to summarystatus enum

Revision ID: 03b238c41f96
Revises: 0f4318f45e85
Create Date: 2026-06-18 16:59:14.027205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03b238c41f96'
down_revision: Union[str, Sequence[str], None] = '0f4318f45e85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("COMMIT")
    # Add 'generating' if it doesn't already exist
    op.execute("ALTER TYPE summarystatus ADD VALUE 'GENERATING'")
    # Add 'failed' if it doesn't already exist
    op.execute("ALTER TYPE summarystatus ADD VALUE 'FAILED'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
