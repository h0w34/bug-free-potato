"""empty message

Revision ID: f38f322aa74d
Revises: 6bfeec6c11a1
Create Date: 2024-06-13 09:26:51.381678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f38f322aa74d'
down_revision = '6bfeec6c11a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
