"""Update driver details

Revision ID: 868c2adca258
Revises: 537701cdcb89
Create Date: 2024-11-15 11:04:46.372833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from app.core.config import settings



# revision identifiers, used by Alembic.
revision: str = '868c2adca258'
down_revision: Union[str, None] = '537701cdcb89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f"""
        ALTER TABLE {settings.DATABASE_ORDER_TABLE}
        ALTER COLUMN delivery_person_id TYPE INTEGER
        USING delivery_person_id::integer
    """)
    op.add_column(f"{settings.DATABASE_ORDER_TABLE}", sa.Column('delivery_person_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.alter_column(f"{settings.DATABASE_ORDER_TABLE}", 'delivery_person_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True,
               server_default=None)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(f"{settings.DATABASE_ORDER_TABLE}", 'delivery_person_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_column(f"{settings.DATABASE_ORDER_TABLE}", 'delivery_person_name')
    # ### end Alembic commands ###
