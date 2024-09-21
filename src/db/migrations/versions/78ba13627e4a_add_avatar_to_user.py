"""add avatar to user

Revision ID: 78ba13627e4a
Revises: afa95c2fb3f3
Create Date: 2024-08-04 20:45:19.041726

"""

import sqlalchemy as sa
from alembic import op

revision = "78ba13627e4a"
down_revision = "afa95c2fb3f3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("avatar_url", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "avatar_url")
    # ### end Alembic commands ###
