"""post image

Revision ID: c89c5c21e0cb
Revises: 5c27fdcaf408
Create Date: 2023-11-19 14:42:07.594919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c89c5c21e0cb'
down_revision = '5c27fdcaf408'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_image', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('post_image')

    # ### end Alembic commands ###