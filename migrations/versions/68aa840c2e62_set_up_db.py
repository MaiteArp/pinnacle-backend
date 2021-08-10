"""set up DB

Revision ID: 68aa840c2e62
Revises: 
Create Date: 2021-07-30 00:13:19.610442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68aa840c2e62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('coins', sa.Integer(), nullable=True),
    sa.Column('best_time', sa.Interval(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('challenge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('challenger_id', sa.Integer(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.Column('winner', sa.Integer(), nullable=True),
    sa.Column('cha_time', sa.Interval(), nullable=True),
    sa.Column('sent_time', sa.Interval(), nullable=True),
    sa.ForeignKeyConstraint(['challenger_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['destination_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('preference',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'key')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    op.drop_table('preference')
    op.drop_table('challenge')
    op.drop_table('user')
    # ### end Alembic commands ###
