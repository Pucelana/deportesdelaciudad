"""pucela

Revision ID: 6c0e912e244c
Revises: c0aec13066d3
Create Date: 2025-05-13 14:46:44.049472

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6c0e912e244c'
down_revision = 'c0aec13066d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('valladolid_partidos', schema=None) as batch_op:
        batch_op.alter_column('hora',
               existing_type=postgresql.TIME(),
               type_=sa.String(length=25),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('valladolid_partidos', schema=None) as batch_op:
        batch_op.alter_column('hora',
               existing_type=sa.String(length=25),
               type_=postgresql.TIME(),
               nullable=False)

    # ### end Alembic commands ###
