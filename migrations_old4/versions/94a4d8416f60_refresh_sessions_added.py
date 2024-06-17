"""refresh sessions added

Revision ID: 94a4d8416f60
Revises: 36b5accd6d32
Create Date: 2024-06-17 11:16:45.198305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94a4d8416f60'
down_revision = '36b5accd6d32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_sessions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('refresh_token', sa.UUID(), nullable=False),
    sa.Column('ua', sa.String(length=200), nullable=False),
    sa.Column('fingerprint', sa.String(length=200), nullable=False),
    sa.Column('ip', sa.String(length=15), nullable=False),
    sa.Column('expires_in', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_sessions')
    # ### end Alembic commands ###