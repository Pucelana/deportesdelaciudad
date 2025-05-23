"""panteras

Revision ID: 9bd19612d32c
Revises: b7b98841634e
Create Date: 2025-05-18 17:34:02.363278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bd19612d32c'
down_revision = 'b7b98841634e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clasificacion_euro_panteras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grupo', sa.String(length=50), nullable=True),
    sa.Column('equipo', sa.String(length=50), nullable=True),
    sa.Column('jugados', sa.Integer(), nullable=True),
    sa.Column('ganados', sa.Integer(), nullable=True),
    sa.Column('perdidos', sa.Integer(), nullable=True),
    sa.Column('puntos', sa.Integer(), nullable=True),
    sa.Column('bonus', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('copa_panteras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eliminatoria', sa.String(length=20), nullable=False),
    sa.Column('fecha', sa.String(length=20), nullable=True),
    sa.Column('hora', sa.String(length=10), nullable=True),
    sa.Column('local', sa.String(length=100), nullable=True),
    sa.Column('bonusA', sa.String(length=120), nullable=True),
    sa.Column('resultadoA', sa.String(length=10), nullable=True),
    sa.Column('resultadoB', sa.String(length=10), nullable=True),
    sa.Column('bonusB', sa.String(length=120), nullable=True),
    sa.Column('visitante', sa.String(length=100), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('europa_panteras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encuentros', sa.String(length=20), nullable=False),
    sa.Column('fecha', sa.String(length=20), nullable=True),
    sa.Column('hora', sa.String(length=10), nullable=True),
    sa.Column('local', sa.String(length=100), nullable=True),
    sa.Column('bonusA', sa.String(length=120), nullable=True),
    sa.Column('resultadoA', sa.String(length=10), nullable=True),
    sa.Column('resultadoB', sa.String(length=10), nullable=True),
    sa.Column('bonusB', sa.String(length=120), nullable=True),
    sa.Column('visitante', sa.String(length=100), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jornadas_panteras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('panteras_clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playoff_panteras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eliminatoria', sa.String(length=20), nullable=False),
    sa.Column('fecha', sa.String(length=20), nullable=True),
    sa.Column('hora', sa.String(length=10), nullable=True),
    sa.Column('local', sa.String(length=100), nullable=True),
    sa.Column('bonusA', sa.String(length=120), nullable=True),
    sa.Column('resultadoA', sa.String(length=10), nullable=True),
    sa.Column('resultadoB', sa.String(length=10), nullable=True),
    sa.Column('bonusB', sa.String(length=120), nullable=True),
    sa.Column('visitante', sa.String(length=100), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supercopa_panteras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eliminatoria', sa.String(length=20), nullable=False),
    sa.Column('fecha', sa.String(length=20), nullable=True),
    sa.Column('hora', sa.String(length=10), nullable=True),
    sa.Column('local', sa.String(length=100), nullable=True),
    sa.Column('bonusA', sa.String(length=120), nullable=True),
    sa.Column('resultadoA', sa.String(length=10), nullable=True),
    sa.Column('resultadoB', sa.String(length=10), nullable=True),
    sa.Column('bonusB', sa.String(length=120), nullable=True),
    sa.Column('visitante', sa.String(length=100), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('panteras_partidos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jornada_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.String(length=20), nullable=True),
    sa.Column('hora', sa.String(length=20), nullable=True),
    sa.Column('local', sa.String(length=255), nullable=True),
    sa.Column('bonusA', sa.String(length=120), nullable=True),
    sa.Column('resultadoA', sa.String(length=120), nullable=True),
    sa.Column('resultadoB', sa.String(length=120), nullable=True),
    sa.Column('bonusB', sa.String(length=120), nullable=True),
    sa.Column('visitante', sa.String(length=255), nullable=True),
    sa.Column('orden', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['jornada_id'], ['jornadas_panteras.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('panteras_partidos')
    op.drop_table('supercopa_panteras')
    op.drop_table('playoff_panteras')
    op.drop_table('panteras_clubs')
    op.drop_table('jornadas_panteras')
    op.drop_table('europa_panteras')
    op.drop_table('copa_panteras')
    op.drop_table('clasificacion_euro_panteras')
    # ### end Alembic commands ###
