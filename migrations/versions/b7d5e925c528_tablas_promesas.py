"""tablas_promesas

Revision ID: b7d5e925c528
Revises: c0f0cb1292ff
Create Date: 2025-04-11 16:11:19.451123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7d5e925c528'
down_revision = 'c0f0cb1292ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jornada_promesas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playoff_promesas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eliminatoria', sa.String(length=20), nullable=False),
    sa.Column('fecha', sa.String(length=20), nullable=True),
    sa.Column('hora', sa.String(length=10), nullable=True),
    sa.Column('local', sa.String(length=100), nullable=True),
    sa.Column('resultadoA', sa.String(length=10), nullable=True),
    sa.Column('resultadoB', sa.String(length=10), nullable=True),
    sa.Column('visitante', sa.String(length=100), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promesas_clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promesas_partidos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jornada_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.String(length=25), nullable=True),
    sa.Column('hora', sa.Time(), nullable=False),
    sa.Column('local', sa.String(length=255), nullable=True),
    sa.Column('resultadoA', sa.String(length=120), nullable=True),
    sa.Column('resultadoB', sa.String(length=120), nullable=True),
    sa.Column('visitante', sa.String(length=255), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['jornada_id'], ['jornada_promesas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promesas_partidos')
    op.drop_table('promesas_clubs')
    op.drop_table('playoff_promesas')
    op.drop_table('jornada_promesas')
    # ### end Alembic commands ###
