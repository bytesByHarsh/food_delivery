"""User Address

Revision ID: 80f2756fc73b
Revises: c259834fc460
Create Date: 2024-11-02 20:11:56.877433

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from app.core.config import settings


# revision identifiers, used by Alembic.
revision: str = "80f2756fc73b"
down_revision: Union[str, None] = "c259834fc460"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

useraddresstype_enum_name = "useraddresstype_enum"
useraddresstype_enum = sa.Enum(
    "HOME", "OFFICE", "OTHER", name=f"{useraddresstype_enum_name}"
)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f"DROP TYPE IF EXISTS {useraddresstype_enum_name}")

    op.create_table(
        f"{settings.DATABASE_USER_ADDRESS_TABLE}",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("address_line_1", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("address_line_2", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("city", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("state", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("postal_code", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("country", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("add_type", useraddresstype_enum, nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            [f"{settings.DATABASE_USER_TABLE}.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f(f"ix_{settings.DATABASE_USER_ADDRESS_TABLE}_id"),
        f"{settings.DATABASE_USER_ADDRESS_TABLE}",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f(f"ix_{settings.DATABASE_USER_ADDRESS_TABLE}_is_deleted"),
        f"{settings.DATABASE_USER_ADDRESS_TABLE}",
        ["is_deleted"],
        unique=False,
    )
    op.add_column(
        f"{settings.DATABASE_USER_TABLE}",
        sa.Column(
            "phone",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="",
        ),
    )
    op.create_index(
        op.f(f"ix_{settings.DATABASE_USER_TABLE}_phone"),
        f"{settings.DATABASE_USER_TABLE}",
        ["phone"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f(f"ix_{settings.DATABASE_USER_TABLE}_phone"),
        table_name=f"{settings.DATABASE_USER_TABLE}",
    )
    op.drop_column(f"{settings.DATABASE_USER_TABLE}", "phone")
    op.drop_index(
        op.f(f"ix_{settings.DATABASE_USER_ADDRESS_TABLE}_is_deleted"),
        table_name=f"{settings.DATABASE_USER_ADDRESS_TABLE}",
    )
    op.drop_index(
        op.f(f"ix_{settings.DATABASE_USER_ADDRESS_TABLE}_id"),
        table_name=f"{settings.DATABASE_USER_ADDRESS_TABLE}",
    )
    op.drop_table(f"{settings.DATABASE_USER_ADDRESS_TABLE}")
    # ### end Alembic commands ###
