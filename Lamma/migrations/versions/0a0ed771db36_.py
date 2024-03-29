"""empty message

Revision ID: 0a0ed771db36
Revises: 0290c4db86d4
Create Date: 2019-09-06 18:43:43.077157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a0ed771db36'
down_revision = '0290c4db86d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('chat1', sa.Integer(), nullable=True),
    sa.Column('chat2', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat1'], ['user.id'], ),
    sa.ForeignKeyConstraint(['chat2'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat')
    # ### end Alembic commands ###
