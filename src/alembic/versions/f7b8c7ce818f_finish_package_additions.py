"""Finish package additions

Revision ID: f7b8c7ce818f
Revises: f55c39b62083
Create Date: 2022-05-26 11:05:21.445739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7b8c7ce818f'
down_revision = 'f55c39b62083'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('package', sa.Column('title', sa.String(), nullable=True))
    op.create_index(op.f('ix_package_title'), 'package', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_package_title'), table_name='package')
    op.drop_column('package', 'title')
    # ### end Alembic commands ###