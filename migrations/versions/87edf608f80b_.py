"""empty message

Revision ID: 87edf608f80b
Revises: e76f5858048f
Create Date: 2024-06-08 02:14:25.083415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87edf608f80b'
down_revision = 'e76f5858048f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('duty_replacements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('duty_id', sa.Integer(), nullable=False),
    sa.Column('replaced_id', sa.Integer(), nullable=False),
    sa.Column('replacing_id', sa.Integer(), nullable=False),
    sa.Column('duty_role_id', sa.Integer(), nullable=False),
    sa.Column('replacement_type_id', sa.Integer(), nullable=True),
    sa.Column('contents', sa.String(length=500), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['duty_id'], ['duties.id'], ),
    sa.ForeignKeyConstraint(['duty_role_id'], ['duty_roles.id'], ),
    sa.ForeignKeyConstraint(['replaced_id'], ['cadets.id'], ),
    sa.ForeignKeyConstraint(['replacement_type_id'], ['replacement_types.id'], ),
    sa.ForeignKeyConstraint(['replacing_id'], ['cadets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('duty_replaces')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('duty_replaces',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('duty_id', sa.INTEGER(), nullable=False),
    sa.Column('replaced_id', sa.INTEGER(), nullable=False),
    sa.Column('replacing_id', sa.INTEGER(), nullable=False),
    sa.Column('duty_role_id', sa.INTEGER(), nullable=False),
    sa.Column('replacement_type_id', sa.INTEGER(), nullable=True),
    sa.Column('contents', sa.VARCHAR(length=500), nullable=True),
    sa.Column('start_date', sa.DATE(), nullable=True),
    sa.Column('end_date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['duty_id'], ['duties.id'], ),
    sa.ForeignKeyConstraint(['duty_role_id'], ['duty_roles.id'], ),
    sa.ForeignKeyConstraint(['replaced_id'], ['cadets.id'], ),
    sa.ForeignKeyConstraint(['replacement_type_id'], ['replacement_types.id'], ),
    sa.ForeignKeyConstraint(['replacing_id'], ['cadets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('duty_replacements')
    # ### end Alembic commands ###
