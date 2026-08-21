"""aliados

Revision ID: d365f46dcdd5
Revises: 7a02fd9f89cb
Create Date: 2026-08-19 21:34:59.233194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd365f46dcdd5'
down_revision = '7a02fd9f89cb'
branch_labels = None
depends_on = None


def upgrade():
    # Añadimos fase con un valor por defecto para las jornadas existentes.
    with op.batch_alter_table('jornadas_aliados', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'fase',
                sa.String(length=30),
                nullable=False,
                server_default='primera_fase'
            )
        )

    # Quitamos el valor por defecto.
    with op.batch_alter_table('jornadas_aliados', schema=None) as batch_op:
        batch_op.alter_column(
            'fase',
            server_default=None
        )


def downgrade():
    with op.batch_alter_table('jornadas_aliados', schema=None) as batch_op:
        batch_op.drop_column('fase')

    # ### end Alembic commands ###
