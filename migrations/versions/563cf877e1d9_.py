"""empty message

Revision ID: 563cf877e1d9
Revises: 29a63cf4f53c
Create Date: 2021-06-10 11:08:54.152432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '563cf877e1d9'
down_revision = '29a63cf4f53c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###
