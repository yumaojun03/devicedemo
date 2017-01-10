# zhangguoqing
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Create device table

Revision ID: e7f6a2fc5d53
Revises: None
Create Date: 2016-11-17 15:41:05.925238

"""

# revision identifiers, used by Alembic.
revision = 'e7f6a2fc5d53'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'device',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('device_id', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(64), nullable=False, unique=True),
        sa.Column('dtype', sa.String(255)),
        sa.Column('vendor', sa.String(255)),
        sa.Column('version', sa.String(255)),
    )


def downgrade():
    op.drop_table('device')
