"""Payment UUID

Revision ID: 6c898a1d906f
Revises: 068aa0a49d78
Create Date: 2024-11-09 20:57:29.481534

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.config import settings


# revision identifiers, used by Alembic.
revision: str = "6c898a1d906f"
down_revision: Union[str, None] = "068aa0a49d78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(f"{settings.DATABASE_ORDER_ITEM_TABLE}", "payment_id")
    op.add_column(
        f"{settings.DATABASE_ORDER_TABLE}",
        sa.Column("payment_id", sa.Uuid(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(f"{settings.DATABASE_ORDER_TABLE}", "payment_id")
    op.add_column(
        f"{settings.DATABASE_ORDER_ITEM_TABLE}",
        sa.Column("payment_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
