"""change timestamp columns to current date

Revision ID: 43569c933ff1
Revises: 86d4e3e3b030
Create Date: 2023-01-07 00:22:23.877329

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '43569c933ff1'
down_revision = '86d4e3e3b030'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stocklogs', 'arrival_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocklogs', sa.Column('arrival_date', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
