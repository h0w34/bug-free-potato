"""empty message

Revision ID: 4c02f74bbd67
Revises: 767c650d5cd8
Create Date: 2024-06-17 13:35:04.017378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c02f74bbd67'
down_revision = '767c650d5cd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('refresh_sessions', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('refresh_token_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('ua',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('fingerprint',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)

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
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
        batch_op.alter_column('fingerprint',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('ua',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('refresh_token_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    # ### end Alembic commands ###
