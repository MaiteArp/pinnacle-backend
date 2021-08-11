"""empty message

Revision ID: b325f36f9557
Revises: 68aa840c2e62
Create Date: 2021-08-11 00:18:50.895147

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b325f36f9557'
down_revision = '68aa840c2e62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('challenge', 'cha_time')
    op.drop_column('challenge', 'sent_time')
    op.drop_column('user', 'best_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('best_time', postgresql.INTERVAL(), autoincrement=False, nullable=True))
    op.add_column('challenge', sa.Column('sent_time', postgresql.INTERVAL(), autoincrement=False, nullable=True))
    op.add_column('challenge', sa.Column('cha_time', postgresql.INTERVAL(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###