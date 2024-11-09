"""Order Details

Revision ID: d65cd3f19a83
Revises: 80f2756fc73b
Create Date: 2024-11-09 16:39:05.759605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from app.core.config import settings



# revision identifiers, used by Alembic.
revision: str = 'd65cd3f19a83'
down_revision: Union[str, None] = '80f2756fc73b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

order_status_enum_name = "order_status_enum"
order_status_enum = sa.Enum('PLACED', 'ORDERED', 'ACCEPTED', 'READY_FOR_PICKUP',
                               'ON_THE_WAY', 'REACHED', 'DELIVERED', 'CANCELLED',
                               'RETURNED', 'FAILED',
                               name=f'{order_status_enum_name}')

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f"DROP TYPE IF EXISTS {order_status_enum_name}")

    op.create_table(f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('order_item_id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}_id'), f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}', ['id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}_is_deleted'), f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}', ['is_deleted'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}_order_item_id'), f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}', ['order_item_id'], unique=False)
    op.create_table(f'{settings.DATABASE_ORDER_ITEM_TABLE}',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('payment_id', sa.Uuid(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price_per_unit', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_TABLE}_id'), f'{settings.DATABASE_ORDER_ITEM_TABLE}', ['id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_TABLE}_is_deleted'), f'{settings.DATABASE_ORDER_ITEM_TABLE}', ['is_deleted'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_TABLE}_order_id'), f'{settings.DATABASE_ORDER_ITEM_TABLE}', ['order_id'], unique=False)
    op.create_table(f'{settings.DATABASE_ORDER_TABLE}',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('customer_id', sa.Uuid(), nullable=False),
    sa.Column('status', order_status_enum, nullable=False),
    sa.Column('food_rating', sa.Integer(), nullable=True),
    sa.Column('delivery_rating', sa.Integer(), nullable=True),
    sa.Column('delivery_person_id', sa.Uuid(), nullable=True),
    sa.Column('address_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], [f'{settings.DATABASE_USER_ADDRESS_TABLE}.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_customer_id'), f'{settings.DATABASE_ORDER_TABLE}', ['customer_id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_id'), f'{settings.DATABASE_ORDER_TABLE}', ['id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_is_deleted'), f'{settings.DATABASE_ORDER_TABLE}', ['is_deleted'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_is_deleted'), table_name=f'{settings.DATABASE_ORDER_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_id'), table_name=f'{settings.DATABASE_ORDER_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_customer_id'), table_name=f'{settings.DATABASE_ORDER_TABLE}')
    op.drop_table('{settings.DATABASE_ORDER_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_TABLE}_order_id'), table_name=f'{settings.DATABASE_ORDER_ITEM_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_TABLE}_is_deleted'), table_name=f'{settings.DATABASE_ORDER_ITEM_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_TABLE}_id'), table_name=f'{settings.DATABASE_ORDER_ITEM_TABLE}')
    op.drop_table('{settings.DATABASE_ORDER_ITEM_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}_order_item_id'), table_name=f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}_is_deleted'), table_name=f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}_id'), table_name=f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}')
    op.drop_table(f'{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}')
    # ### end Alembic commands ###
