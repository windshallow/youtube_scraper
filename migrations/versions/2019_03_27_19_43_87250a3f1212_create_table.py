# -*- coding: utf-8 -*-

"""create table

Revision ID: 87250a3f1212
Revises: 
Create Date: 2019-03-27 19:43:19.503787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87250a3f1212'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 添加表
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

    # 添加列
    # op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    # 删除表
    op.drop_table('account')

    # 删除列
    # op.drop_column('account', 'last_transaction_date')
