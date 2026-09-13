"""fix cascade

Revision ID: 2f200b72e49f
Revises: 
Create Date: 2026-08-30 14:47:09.409212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f200b72e49f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "books_author_id_fkey",
        "books",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "books_author_id_fkey",
        "books",
        "authors",
        ["author_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(
        "books_author_id_fkey",
        "books",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "books_author_id_fkey",
        "books",
        "authors",
        ["author_id"],
        ["id"]
    )