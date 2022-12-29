"""init db schemas

Revision ID: 025dd432613f
Revises: 
Create Date: 2022-12-24 23:46:56.683691

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '025dd432613f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sales_logs',
    sa.Column('date_sold', sa.DateTime(), nullable=False),
    sa.Column('no_of_sales', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('date_sold')
    )
    op.create_table('stock_available',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('size_range', mysql.LONGTEXT(), nullable=False),
    sa.Column('colours', mysql.LONGTEXT(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('variation', mysql.LONGTEXT(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stocklogs',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('size_range', mysql.LONGTEXT(), nullable=False),
    sa.Column('colours', mysql.LONGTEXT(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('variation', mysql.LONGTEXT(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('arrival_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('user',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('stocklogs')
    op.drop_table('stock_available')
    op.drop_table('sales_logs')
    # ### end Alembic commands ###
