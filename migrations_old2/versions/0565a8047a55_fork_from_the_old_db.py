"""fork from the old db

Revision ID: 0565a8047a55
Revises: 
Create Date: 2024-05-24 22:05:08.138624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0565a8047a55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('positions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ranks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rank_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('ak_cells',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('duty_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faculties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('pm_cells',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_user_id'), ['user_id'], unique=False)

    op.create_table('role_user',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('faculty_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('duties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('duty_type_id', sa.Integer(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['duty_type_id'], ['duty_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('duty_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('duty_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['duty_type_id'], ['duty_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('number_of_cadets', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('faculty_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cadets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('patronymic', sa.String(length=50), nullable=True),
    sa.Column('rank_id', sa.Integer(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('pm_cell_id', sa.Integer(), nullable=True),
    sa.Column('ak_cell_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('faculty_id', sa.Integer(), nullable=True),
    sa.Column('main_location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ak_cell_id'], ['ak_cells.id'], ),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculties.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['main_location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['pm_cell_id'], ['pm_cells.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ),
    sa.ForeignKeyConstraint(['rank_id'], ['ranks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cadet_duty',
    sa.Column('cadet_id', sa.Integer(), nullable=False),
    sa.Column('duty_id', sa.Integer(), nullable=False),
    sa.Column('duty_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cadet_id'], ['cadets.id'], ),
    sa.ForeignKeyConstraint(['duty_id'], ['duties.id'], ),
    sa.ForeignKeyConstraint(['duty_role_id'], ['duty_roles.id'], ),
    sa.PrimaryKeyConstraint('cadet_id', 'duty_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cadet_duty')
    op.drop_table('cadets')
    op.drop_table('groups')
    op.drop_table('duty_roles')
    op.drop_table('duties')
    op.drop_table('courses')
    op.drop_table('role_user')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_user_id'))
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    op.drop_table('pm_cells')
    op.drop_table('followers')
    op.drop_table('faculties')
    op.drop_table('duty_types')
    op.drop_table('ak_cells')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('roles')
    op.drop_table('ranks')
    op.drop_table('positions')
    op.drop_table('locations')
    # ### end Alembic commands ###
