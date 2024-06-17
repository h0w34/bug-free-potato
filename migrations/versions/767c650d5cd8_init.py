"""init

Revision ID: 767c650d5cd8
Revises: 
Create Date: 2024-06-17 13:23:07.120136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767c650d5cd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('refresh_sessions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('refresh_token_id', sa.UUID(), nullable=False))
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.drop_column('refresh_token')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('refresh_sessions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('refresh_token', sa.VARCHAR(length=400), nullable=False))
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.drop_column('refresh_token_id')

    # ### end Alembic commands ###