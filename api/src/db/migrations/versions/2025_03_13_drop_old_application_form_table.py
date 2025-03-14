"""Drop old application form table

Revision ID: 3793197bdd1b
Revises: 5268c5f97814
Create Date: 2025-03-13 15:54:04.363455

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3793197bdd1b"
down_revision = "5268c5f97814"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "competition_form_form_id_application_form_fkey",
        "competition_form",
        schema="api",
        type_="foreignkey",
    )
    op.drop_table("application_form", schema="api")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "application_form",
        sa.Column("form_id", sa.UUID(), nullable=False),
        sa.Column("form_name", sa.Text(), nullable=False),
        sa.Column("form_version", sa.Text(), nullable=False),
        sa.Column("agency_code", sa.Text(), nullable=False),
        sa.Column("omb_number", sa.Text(), nullable=True),
        sa.Column("active_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("inactive_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("form_id", name=op.f("application_form_pkey")),
        schema="api",
    )
    # ### end Alembic commands ###
