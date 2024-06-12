"""replacements models upgr

Revision ID: 1576efdfcefc
Revises: 87edf608f80b
Create Date: 2024-06-10 14:01:41.201784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1576efdfcefc'
down_revision = '87edf608f80b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('duty_replacements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('replacement_doc_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('commentary', sa.String(length=300), nullable=True))
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'replacement_docs', ['replacement_doc_id'], ['id'])
        batch_op.drop_column('start_date')
        batch_op.drop_column('end_date')
        batch_op.drop_column('replacement_type_id')
        batch_op.drop_column('contents')

    with op.batch_alter_table('replacement_types', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(length=30),
               type_=sa.String(length=30),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('replacement_types', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=30),
               type_=sa.TEXT(length=30),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('duty_replacements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contents', sa.VARCHAR(length=500), nullable=True))
        batch_op.add_column(sa.Column('replacement_type_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('end_date', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('start_date', sa.DATE(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'replacement_types', ['replacement_type_id'], ['id'])
        batch_op.drop_column('creation_date')
        batch_op.drop_column('commentary')
        batch_op.drop_column('replacement_doc_id')

    # ### end Alembic commands ###
