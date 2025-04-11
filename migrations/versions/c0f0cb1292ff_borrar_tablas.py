"""borrar tablas

Revision ID: c0f0cb1292ff
Revises: 1a16478c693d
Create Date: 2025-04-11 14:59:42.869599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0f0cb1292ff'
down_revision = '1a16478c693d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clasif_copa_valladolid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clasif_copa_valladolid',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('grupo', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('equipo', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('jugados', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ganados', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('empatados', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('perdidos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('puntos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='clasif_copa_valladolid_pkey')
    )
    # ### end Alembic commands ###
