"""recoletas

Revision ID: 640858df2d13
Revises: 41cf021abab7
Create Date: 2025-04-24 20:03:14.465358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '640858df2d13'
down_revision = '41cf021abab7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clasificacion_europa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grupo', sa.String(length=50), nullable=True),
    sa.Column('equipo', sa.String(length=50), nullable=True),
    sa.Column('jugados', sa.Integer(), nullable=True),
    sa.Column('ganados', sa.Integer(), nullable=True),
    sa.Column('perdidos', sa.Integer(), nullable=True),
    sa.Column('puntos', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clasificacion_europa')
    # ### end Alembic commands ###
