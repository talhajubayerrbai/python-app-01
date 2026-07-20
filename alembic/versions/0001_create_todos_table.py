"""retired placeholder - do not use

Revision ID: 0003
Revises: 0002
Create Date: 2025-01-03 00:00:00.000000

This file exists only to prevent Alembic from failing if it was previously
copied to a server. It is a no-op migration at the end of the chain.
"""
from typing import Sequence, Union

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
