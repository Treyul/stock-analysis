"""added stock size variation

Revision ID: 9833cc8d8c90
Revises: c506fd4d5279
Create Date: 2022-10-01 07:37:54.682132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9833cc8d8c90'
down_revision = 'c506fd4d5279'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('stocklogs','size_range',existing_type=sa.JSON,nullable=False)
    


def downgrade():
    op.alter_column('stocklogs','size_range',existing_type=sa.Integer,nullable=False)
