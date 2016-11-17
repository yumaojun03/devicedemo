"""Create user table

Revision ID: ff7b0e8f7372
Revises: 
Create Date: 2016-11-17 13:15:55.839221

"""

# revision identifiers, used by Alembic.
revision = 'ff7b0e8f7372'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(64), nullable=False, unique=True),
        sa.Column('email', sa.String(255))
    )


def downgrade():
    op.drop_table('user')
