"""create fk bought next

Revision ID: 24a02b95fa55
Revises: 8c885d4409ca
Create Date: 2020-07-18 00:33:03.337490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24a02b95fa55'
down_revision = '8c885d4409ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('usually_bought_next_ibfk_1', 'usually_bought_next', 'product', ['product_id'], ['product_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('usually_bought_next_ibfk_1', 'usually_bought_next', type_='foreignkey')
    # ### end Alembic commands ###
