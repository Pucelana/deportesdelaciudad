"""Cambio

Revision ID: e98f3d637e4e
Revises: 2703e857a343
Create Date: 2026-05-05 19:38:13.908465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e98f3d637e4e'
down_revision = '2703e857a343'
branch_labels = None
depends_on = None

def upgrade():

    with op.batch_alter_table('playoff_uemc', schema=None) as batch_op:

        batch_op.execute("""
            UPDATE playoff_uemc
            SET "resultadoA" = NULL
            WHERE "resultadoA" = ''
        """)

        batch_op.execute("""
            UPDATE playoff_uemc
            SET "resultadoB" = NULL
            WHERE "resultadoB" = ''
        """)

        batch_op.alter_column(
            'resultadoA',
            existing_type=sa.VARCHAR(length=10),
            type_=sa.Integer(),
            existing_nullable=True,
            postgresql_using='"resultadoA"::integer'
        )

        batch_op.alter_column(
            'resultadoB',
            existing_type=sa.VARCHAR(length=10),
            type_=sa.Integer(),
            existing_nullable=True,
            postgresql_using='"resultadoB"::integer'
        )


def downgrade():

    with op.batch_alter_table('playoff_uemc', schema=None) as batch_op:

        batch_op.alter_column(
            'resultadoA',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True
        )

        batch_op.alter_column(
            'resultadoB',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True
        )

