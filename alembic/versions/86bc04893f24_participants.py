"""participants

Revision ID: 86bc04893f24
Revises: 9031569c7f21
Create Date: 2021-09-04 21:20:28.826279

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "86bc04893f24"
down_revision = "9031569c7f21"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "participants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "player_id",
            sa.Integer(),
            sa.ForeignKey("players.id", ondelete="cascade"),
            nullable=False,
        ),
        sa.Column(
            "tournament_id",
            sa.Integer(),
            sa.ForeignKey("tournaments.id", ondelete="cascade"),
            nullable=False,
        ),
        sa.Column("declared_rating", sa.Numeric(precision=7, scale=3)),
        sa.Column("start_rating", sa.Numeric(precision=7, scale=3)),
        sa.Column("end_rating", sa.Numeric(precision=7, scale=3)),
        sa.UniqueConstraint("player_id", "tournament_id", name="uq_participant"),
    )


def downgrade():
    op.drop_table("participants")
