"""ct_review

Revision ID: 552ee6e5ed04
Revises: f1afd88c2f54
Create Date: 2020-08-19 19:13:57.794247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '552ee6e5ed04'
down_revision = 'f1afd88c2f54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('date', sa.String(length=20), nullable=False),
    sa.Column('text', sa.String(length=2000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    # ### end Alembic commands ###
