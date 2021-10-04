"""

Revision ID: ce349a7ca482
Revises: 86bc04893f24
Create Date: 2021-10-03 16:03:07.420357

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "ce349a7ca482"
down_revision = "86bc04893f24"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
    )


def downgrade():
    op.drop_table("users")
