"""add competition tables

Revision ID: d5f73aa58acb
Revises: 56d129425397
Create Date: 2025-02-19 15:40:40.408114

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d5f73aa58acb"
down_revision = "56d129425397"
branch_labels = None
depends_on = None


def upgrade():
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
    op.create_table(
        "competition_form",
        sa.Column("competition_id", sa.UUID(), nullable=False),
        sa.Column("form_id", sa.UUID(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["api.application_form.form_id"],
            name=op.f("competition_form_form_id_application_form_fkey"),
        ),
        sa.PrimaryKeyConstraint("competition_id", "form_id", name=op.f("competition_form_pkey")),
        schema="api",
    )
    op.create_table(
        "competition",
        sa.Column("competition_id", sa.UUID(), nullable=False),
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("legacy_competition_id", sa.BigInteger(), nullable=True),
        sa.Column("public_competition_id", sa.Text(), nullable=True),
        sa.Column("legacy_package_id", sa.Text(), nullable=True),
        sa.Column("competition_title", sa.Text(), nullable=True),
        sa.Column("opening_date", sa.Date(), nullable=True),
        sa.Column("closing_date", sa.Date(), nullable=True),
        sa.Column("grace_period", sa.BigInteger(), nullable=True),
        sa.Column("contact_info", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("competition_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint("competition_id", name=op.f("competition_pkey")),
        schema="api",
    )
    op.create_index(
        op.f("competition_legacy_competition_id_idx"),
        "competition",
        ["legacy_competition_id"],
        unique=False,
        schema="api",
    )
    op.create_index(
        op.f("competition_opportunity_id_idx"),
        "competition",
        ["opportunity_id"],
        unique=False,
        schema="api",
    )
    op.create_table(
        "competition_assistance_listing",
        sa.Column("competition_id", sa.UUID(), nullable=False),
        sa.Column("opportunity_assistance_listing_id", sa.BigInteger(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["competition_id"],
            ["api.competition.competition_id"],
            name=op.f("competition_assistance_listing_competition_id_competition_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_assistance_listing_id"],
            ["api.opportunity_assistance_listing.opportunity_assistance_listing_id"],
            name=op.f(
                "competition_assistance_listing_opportunity_assistance_listing_id_opportunity_assistance_listing_fkey"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "competition_id",
            "opportunity_assistance_listing_id",
            name=op.f("competition_assistance_listing_pkey"),
        ),
        schema="api",
    )
    op.create_table(
        "competition_instruction",
        sa.Column("competition_instruction_id", sa.UUID(), nullable=False),
        sa.Column("competition_id", sa.UUID(), nullable=False),
        sa.Column("file_location", sa.Text(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["competition_id"],
            ["api.competition.competition_id"],
            name=op.f("competition_instruction_competition_id_competition_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "competition_instruction_id",
            "competition_id",
            name=op.f("competition_instruction_pkey"),
        ),
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("competition_instruction", schema="api")
    op.drop_table("competition_assistance_listing", schema="api")
    op.drop_index(op.f("competition_opportunity_id_idx"), table_name="competition", schema="api")
    op.drop_index(
        op.f("competition_legacy_competition_id_idx"), table_name="competition", schema="api"
    )
    op.drop_table("competition", schema="api")
    op.drop_table("competition_form", schema="api")
    op.drop_table("application_form", schema="api")
    # ### end Alembic commands ###
