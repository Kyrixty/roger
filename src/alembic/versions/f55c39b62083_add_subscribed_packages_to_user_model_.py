"""Add subscribed_packages to user model + establish relationship between subscribed_packages and Package model

Revision ID: f55c39b62083
Revises: bcaffd1e3d19
Create Date: 2022-05-26 10:51:23.965924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f55c39b62083'
down_revision = 'bcaffd1e3d19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('subscribed_packages', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'package', ['subscribed_packages'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'subscribed_packages')
    # ### end Alembic commands ###
