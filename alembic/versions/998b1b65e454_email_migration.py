"""email migration

Revision ID: 998b1b65e454
Revises: 5c4b0575bba3
Create Date: 2025-11-11 15:53:28.031812
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = '998b1b65e454'
down_revision: Union[str, None] = '5c4b0575bba3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: convert todos datetime columns to timezone-aware"""
    # Convert due_date column
    op.alter_column(
        'todos',
        'due_date',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        postgresql_using="due_date::timestamp with time zone"
    )

    # Convert created_at column
    op.alter_column(
        'todos',
        'created_at',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        postgresql_using="created_at::timestamp with time zone"
    )

    # Convert updated_at column
    op.alter_column(
        'todos',
        'updated_at',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        postgresql_using="updated_at::timestamp with time zone"
    )


def downgrade() -> None:
    """Revert schema: convert todos datetime columns back to string"""
    op.alter_column(
        'todos',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False
    )

    op.alter_column(
        'todos',
        'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False
    )

    op.alter_column(
        'todos',
        'due_date',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False
    )
