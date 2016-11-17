"""Create device table

Revision ID: e7f6a2fc5d53
Revises: ff7b0e8f7372
Create Date: 2016-11-17 15:41:05.925238

"""

# revision identifiers, used by Alembic.
revision = 'e7f6a2fc5d53'
down_revision = 'ff7b0e8f7372'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'device',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('uuid', sa.String(255), nullable=False),
        sa.Column('name', sa.String(64), nullable=False, unique=True),
        sa.Column('type', sa.String(255)),
        sa.Column('vendor', sa.String(255)),
        sa.Column('version', sa.String(255)),
    )


def downgrade():
    op.drop_table('device')
