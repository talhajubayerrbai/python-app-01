"""rename tasks table to todos

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("tasks", "todos")
    op.execute("ALTER INDEX ix_tasks_id RENAME TO ix_todos_id")


def downgrade() -> None:
    op.execute("ALTER INDEX ix_todos_id RENAME TO ix_tasks_id")
    op.rename_table("todos", "tasks")
