"""added Role and User models

Revision ID: 7446f7958a9f
Revises: 7b9fe89befbf
Create Date: 2020-04-07 16:10:25.081773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7446f7958a9f'
down_revision = '7b9fe89befbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('user_coordinates')
    op.drop_table('userDT')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userDT',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('dt_start', sa.VARCHAR(), nullable=False),
    sa.Column('dt_finish', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_coordinates',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('latitude', sa.VARCHAR(), nullable=False),
    sa.Column('longitude', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
