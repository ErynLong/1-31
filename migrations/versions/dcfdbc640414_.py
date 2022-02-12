"""empty message

Revision ID: dcfdbc640414
Revises: 393d29e2ec45
Create Date: 2022-02-11 20:42:08.634413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcfdbc640414'
down_revision = '393d29e2ec45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokedata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('defense', sa.String(length=50), nullable=True),
    sa.Column('attack', sa.String(length=50), nullable=True),
    sa.Column('ability_1', sa.String(length=50), nullable=True),
    sa.Column('ability_2', sa.String(length=50), nullable=True),
    sa.Column('sprite', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_pokedata',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pokedata_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pokedata_id'], ['pokedata.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'pokedata_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_pokedata')
    op.drop_table('pokedata')
    # ### end Alembic commands ###