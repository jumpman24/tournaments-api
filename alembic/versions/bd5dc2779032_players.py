""" Players table

Revision ID: bd5dc2779032
Revises:
Create Date: 2021-08-26 13:44:04.487670

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "bd5dc2779032"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("last_name", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("rating", sa.Numeric(7, 3), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
    )


def downgrade():
    op.drop_table("players")
