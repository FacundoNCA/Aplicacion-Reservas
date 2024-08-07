"""Borrar en cascada las reservas cuando se elimina el cliente

Revision ID: a78734b919eb
Revises: 
Create Date: 2024-07-21 19:15:18.756366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a78734b919eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('reservas', schema=None) as batch_op:
        batch_op.drop_constraint('reservas_id_cliente_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'clientes', ['id_cliente'], ['id_cliente'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservas', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('reservas_id_cliente_fkey', 'clientes', ['id_cliente'], ['id_cliente'])

    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
