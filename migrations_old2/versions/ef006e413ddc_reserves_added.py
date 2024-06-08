"""reserves added

Revision ID: ef006e413ddc
Revises: 0565a8047a55
Create Date: 2024-06-03 16:31:15.023721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef006e413ddc'
down_revision = '0565a8047a55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserve_cadet_duties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('duty_id', sa.Integer(), nullable=False),
    sa.Column('cadet_id', sa.Integer(), nullable=False),
    sa.Column('duty_role_id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cadet_id'], ['cadets.id'], ),
    sa.ForeignKeyConstraint(['duty_id'], ['duties.id'], ),
    sa.ForeignKeyConstraint(['duty_role_id'], ['duty_roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cadets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sex', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cadets', schema=None) as batch_op:
        batch_op.drop_column('sex')

    op.drop_table('reserve_cadet_duties')
    # ### end Alembic commands ###