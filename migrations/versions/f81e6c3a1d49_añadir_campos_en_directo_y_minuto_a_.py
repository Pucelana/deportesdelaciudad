"""añadir campos en_directo y minuto a Horario

Revision ID: f81e6c3a1d49
Revises: 
Create Date: 2025-04-06 18:00:47.652928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f81e6c3a1d49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('horarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('en_directo', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('minuto', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('horarios', schema=None) as batch_op:
        batch_op.drop_column('minuto')
        batch_op.drop_column('en_directo')

    # ### end Alembic commands ###
