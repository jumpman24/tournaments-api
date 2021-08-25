"""tournaments

Revision ID: 9031569c7f21
Revises: bd5dc2779032
Create Date: 2021-08-31 13:50:53.009856

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "9031569c7f21"
down_revision = "bd5dc2779032"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tournaments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column("date_start", sa.Date(), nullable=False),
        sa.Column("date_end", sa.Date(), nullable=False),
    )


def downgrade():
    op.drop_table("tournaments")
