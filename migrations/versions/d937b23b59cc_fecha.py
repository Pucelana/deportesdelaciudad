"""fecha

Revision ID: d937b23b59cc
Revises: ad055aa411ce
Create Date: 2025-04-11 11:42:31.987182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd937b23b59cc'
down_revision = 'ad055aa411ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('valladolid_partidos', schema=None) as batch_op:
        batch_op.alter_column('fecha',
               existing_type=sa.DATE(),
               type_=sa.String(length=25),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('valladolid_partidos', schema=None) as batch_op:
        batch_op.alter_column('fecha',
               existing_type=sa.String(length=25),
               type_=sa.DATE(),
               nullable=False)

    # ### end Alembic commands ###
