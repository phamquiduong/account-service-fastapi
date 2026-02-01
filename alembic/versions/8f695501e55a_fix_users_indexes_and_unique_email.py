"""fix users indexes and unique email

Revision ID: 8f695501e55a
Revises: 68bbe7c36dcf
Create Date: 2026-02-01 17:05:15.630869

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8f695501e55a"
down_revision: Union[str, Sequence[str], None] = "68bbe7c36dcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_index("ix_users_created_at", table_name="users")
    op.drop_index("ix_users_updated_at", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.create_unique_constraint("uq_users_email", "users", ["email"])
    op.create_index("ix_users_email", "users", ["email"])


def downgrade():
    op.drop_index("ix_users_email", table_name="users")
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_created_at", "users", ["created_at"])
    op.create_index("ix_users_updated_at", "users", ["updated_at"])
