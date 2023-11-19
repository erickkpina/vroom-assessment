"""Remove slug

Revision ID: a96ac8564976
Revises: ad23bdf94f76
Create Date: 2023-11-18 19:10:53.677626

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a96ac8564976'
down_revision = 'ad23bdf94f76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('slug')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', mysql.VARCHAR(length=255), nullable=True))

    # ### end Alembic commands ###