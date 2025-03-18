"""Initial migration

Revision ID: 4ed0c900b6a4
Revises: 30568322bceb
Create Date: 2025-03-17 10:46:45.460661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed0c900b6a4'
down_revision = '30568322bceb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode', sa.String(length=50), nullable=False))
        batch_op.create_unique_constraint('uq_book_barcode', ['barcode'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('uq_book_barcode', type_='unique')
        batch_op.drop_column('barcode')
    # ### end Alembic commands ###
