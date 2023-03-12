"""empty message

Revision ID: 9ac1ddfcee24
Revises: 
Create Date: 2023-03-12 07:44:43.024620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ac1ddfcee24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('match',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('secret_key', sa.UUID(), nullable=True),
    sa.Column('server_id', sa.Text(), nullable=False),
    sa.Column('server_host', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('selected_map', sa.Text(), nullable=False),
    sa.Column('max_rounds', sa.SmallInteger(), nullable=False),
    sa.Column('team1_name', sa.Text(), nullable=False),
    sa.Column('team1_score', sa.SmallInteger(), nullable=True),
    sa.Column('team1_roster', sa.ARRAY(sa.Text()), nullable=False),
    sa.Column('team2_name', sa.Text(), nullable=False),
    sa.Column('team2_score', sa.SmallInteger(), nullable=True),
    sa.Column('team2_roster', sa.ARRAY(sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('match')
