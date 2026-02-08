"""add is_verify_email and is_active to users

Revision ID: 6a04f96853fc
Revises: ff81395e4e04
Create Date: 2026-02-08 19:26:36.185693

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a04f96853fc"
down_revision: Union[str, Sequence[str], None] = "ff81395e4e04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", sa.Column("is_verify_email", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    op.drop_column("users", "is_active")
    op.drop_column("users", "is_verify_email")
