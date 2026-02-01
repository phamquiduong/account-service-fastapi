"""remove duplicate email index

Revision ID: ff81395e4e04
Revises: 8f695501e55a
Create Date: 2026-02-01 17:12:14.825987

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ff81395e4e04"
down_revision: Union[str, Sequence[str], None] = "8f695501e55a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_index("ix_users_email", table_name="users")


def downgrade():
    op.create_index("ix_users_email", "users", ["email"])
