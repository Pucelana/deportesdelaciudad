"""bonus

Revision ID: 925afca70235
Revises: a340cd369b3e
Create Date: 2025-05-17 13:58:30.968524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '925afca70235'
down_revision = 'a340cd369b3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('caja_partidos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bonusA', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('bonusB', sa.String(length=120), nullable=True))

    with op.batch_alter_table('copa_caja', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bonusA', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('bonusB', sa.String(length=120), nullable=True))

    with op.batch_alter_table('europa_caja', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bonusA', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('bonusB', sa.String(length=120), nullable=True))

    with op.batch_alter_table('playoff_caja', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bonusA', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('bonusB', sa.String(length=120), nullable=True))

    with op.batch_alter_table('supercopa_caja', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bonusA', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('bonusB', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('supercopa_caja', schema=None) as batch_op:
        batch_op.drop_column('bonusB')
        batch_op.drop_column('bonusA')

    with op.batch_alter_table('playoff_caja', schema=None) as batch_op:
        batch_op.drop_column('bonusB')
        batch_op.drop_column('bonusA')

    with op.batch_alter_table('europa_caja', schema=None) as batch_op:
        batch_op.drop_column('bonusB')
        batch_op.drop_column('bonusA')

    with op.batch_alter_table('copa_caja', schema=None) as batch_op:
        batch_op.drop_column('bonusB')
        batch_op.drop_column('bonusA')

    with op.batch_alter_table('caja_partidos', schema=None) as batch_op:
        batch_op.drop_column('bonusB')
        batch_op.drop_column('bonusA')

    # ### end Alembic commands ###
