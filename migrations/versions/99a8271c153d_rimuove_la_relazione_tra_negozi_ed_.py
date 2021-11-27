"""Rimuove la relazione tra negozi ed utenti

Revision ID: 99a8271c153d
Revises: 0c78bef9807b
Create Date: 2021-11-27 18:39:05.602907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99a8271c153d'
down_revision = '0c78bef9807b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('negozi', schema=None) as batch_op:
        batch_op.drop_constraint('fk_negozi_titolare_id_utenti', type_='foreignkey')
        batch_op.drop_column('titolare_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('negozi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('titolare_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_negozi_titolare_id_utenti', 'utenti', ['titolare_id'], ['id'])

    # ### end Alembic commands ###
