"""Order Rating

Revision ID: 068aa0a49d78
Revises: d65cd3f19a83
Create Date: 2024-11-09 20:38:38.603919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from app.core.config import settings

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '068aa0a49d78'
down_revision: Union[str, None] = 'd65cd3f19a83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(f'{settings.DATABASE_ORDER_RATING_TABLE}',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('food_rating', sa.Integer(), nullable=True),
    sa.Column('delivery_rating', sa.Integer(), nullable=True),
    sa.Column('delivery_person_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('restaurant_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], [f'{settings.DATABASE_ORDER_TABLE}.id'], ),
    sa.ForeignKeyConstraint(['user_id'], [f'{settings.DATABASE_USER_TABLE}.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_RATING_TABLE}_id'), f'{settings.DATABASE_ORDER_RATING_TABLE}', ['id'], unique=False)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_RATING_TABLE}_is_deleted'), f'{settings.DATABASE_ORDER_RATING_TABLE}', ['is_deleted'], unique=False)
    op.add_column(f'{settings.DATABASE_ORDER_TABLE}', sa.Column('restaurant_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.alter_column(f'{settings.DATABASE_ORDER_TABLE}', 'delivery_person_id',
               existing_type=sa.UUID(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.create_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_restaurant_id'), f'{settings.DATABASE_ORDER_TABLE}', ['restaurant_id'], unique=False)
    op.drop_column(f'{settings.DATABASE_ORDER_TABLE}', 'delivery_rating')
    op.drop_column(f'{settings.DATABASE_ORDER_TABLE}', 'food_rating')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(f'{settings.DATABASE_ORDER_TABLE}', sa.Column('food_rating', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column(f'{settings.DATABASE_ORDER_TABLE}', sa.Column('delivery_rating', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_TABLE}_restaurant_id'), table_name=f'{settings.DATABASE_ORDER_TABLE}')
    op.alter_column(f'{settings.DATABASE_ORDER_TABLE}', 'delivery_person_id',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.UUID(),
               existing_nullable=True)
    op.drop_column(f'{settings.DATABASE_ORDER_TABLE}', 'restaurant_id')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_RATING_TABLE}_is_deleted'), table_name=f'{settings.DATABASE_ORDER_RATING_TABLE}')
    op.drop_index(op.f(f'ix_{settings.DATABASE_ORDER_RATING_TABLE}_id'), table_name=f'{settings.DATABASE_ORDER_RATING_TABLE}')
    op.drop_table(f'{settings.DATABASE_ORDER_RATING_TABLE}')
    # ### end Alembic commands ###