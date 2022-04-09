"""empty message

Revision ID: f24a3a1b6e42
Revises: 
Create Date: 2022-04-09 22:57:49.057084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f24a3a1b6e42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('hsnsac', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('hsnsac', sa.String(), nullable=True),
    sa.Column('pan', sa.String(), nullable=True),
    sa.Column('gstin', sa.String(), nullable=True),
    sa.Column('acs', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_modes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice_headers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_num', sa.String(), nullable=True),
    sa.Column('invoice_date', sa.Date(), nullable=True),
    sa.Column('booking_id', sa.String(), nullable=True),
    sa.Column('booking_date', sa.Date(), nullable=True),
    sa.Column('payee', sa.String(), nullable=True),
    sa.Column('guest', sa.String(), nullable=True),
    sa.Column('guest_details', sa.String(), nullable=True),
    sa.Column('gstin', sa.String(), nullable=True),
    sa.Column('arrive', sa.Date(), nullable=True),
    sa.Column('depart', sa.Date(), nullable=True),
    sa.Column('nights', sa.Integer(), nullable=True),
    sa.Column('rooms', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('hotel_id', sa.Integer(), nullable=True),
    sa.Column('payment_mode_id', sa.Integer(), nullable=True),
    sa.Column('tpr', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('npa', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.ForeignKeyConstraint(['payment_mode_id'], ['payment_modes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice_lines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.Column('charge_id', sa.Integer(), nullable=True),
    sa.Column('hsnsac', sa.String(), nullable=True),
    sa.Column('stay_date', sa.Date(), nullable=True),
    sa.Column('sell_rate', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('inclusion', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('subtotal', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('cgst', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('sgst', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['charge_id'], ['charges.id'], ),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice_headers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice_lines')
    op.drop_table('invoice_headers')
    op.drop_table('sources')
    op.drop_table('payment_modes')
    op.drop_table('hotels')
    op.drop_table('config')
    op.drop_table('charges')
    # ### end Alembic commands ###
