"""Add total pricein order

Revision ID: 537701cdcb89
Revises: 63dc14b49234
Create Date: 2024-11-11 23:48:43.014105

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.config import settings


# revision identifiers, used by Alembic.
revision: str = "537701cdcb89"
down_revision: Union[str, None] = "63dc14b49234"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        f"{settings.DATABASE_ORDER_TABLE}",
        sa.Column("total_cost", sa.Float(), nullable=False, server_default="0.0"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(f"{settings.DATABASE_ORDER_TABLE}", "total_cost")
    # ### end Alembic commands ###
