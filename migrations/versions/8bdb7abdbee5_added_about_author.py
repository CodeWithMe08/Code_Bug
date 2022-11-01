"""added about author

Revision ID: 8bdb7abdbee5
Revises: 07e826111df5
Create Date: 2022-11-01 17:36:21.476922

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8bdb7abdbee5'
down_revision = '07e826111df5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_author', sa.Text(length=500), nullable=True))
    op.drop_column('users', 'favorite_color')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('favorite_color', mysql.VARCHAR(length=120), nullable=True))
    op.drop_column('users', 'about_author')
    # ### end Alembic commands ###
