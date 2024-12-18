"""Init DB

Revision ID: daf69c52c9a8
Revises:
Create Date: 2024-11-15 12:47:12.703193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from app.core.config import settings



# revision identifiers, used by Alembic.
revision: str = 'daf69c52c9a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(f'{settings.DATABASE_RESTAURANT_TABLE}',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('open_hr', sa.Integer(), nullable=False),
    sa.Column('close_hr', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('pincode', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f(f'ix_{settings.DATABASE_RESTAURANT_TABLE}_id'), f'{settings.DATABASE_RESTAURANT_TABLE}', ['id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_RESTAURANT_TABLE}_is_deleted'), f'{settings.DATABASE_RESTAURANT_TABLE}', ['is_deleted'], unique=False)
    op.create_table('items',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('restaurant_id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], [f'{settings.DATABASE_RESTAURANT_TABLE}.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_is_deleted'), 'items', ['is_deleted'], unique=False)
    op.create_table(f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('item_id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f(f'ix_{settings.DATABASE_MENU_ITEM_ADDON_TABLE}_id'), f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}', ['id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_MENU_ITEM_ADDON_TABLE}_is_deleted'), f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}', ['is_deleted'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_MENU_ITEM_ADDON_TABLE}_item_id'), f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}', ['item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f(f'ix_{settings.DATABASE_MENU_ITEM_ADDON_TABLE}_item_id'), table_name=f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_MENU_ITEM_ADDON_TABLE}_is_deleted'), table_name=f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_MENU_ITEM_ADDON_TABLE}_id'), table_name=f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}')
    op.drop_table(f'{settings.DATABASE_MENU_ITEM_ADDON_TABLE}')
    op.drop_index(op.f('ix_items_is_deleted'), table_name='items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f(f'ix_{settings.DATABASE_RESTAURANT_TABLE}_is_deleted'), table_name=f'{settings.DATABASE_RESTAURANT_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_RESTAURANT_TABLE}_id'), table_name=f'{settings.DATABASE_RESTAURANT_TABLE}')
    op.drop_table(f'{settings.DATABASE_RESTAURANT_TABLE}')
    # ### end Alembic commands ###
