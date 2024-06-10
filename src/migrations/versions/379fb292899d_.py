"""empty message

Revision ID: 379fb292899d
Revises: f63c1753779b
Create Date: 2024-06-10 17:44:03.604500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '379fb292899d'
down_revision: Union[str, None] = 'f63c1753779b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('capital_cities', 'country',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('capital_cities', 'city',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('capital_cities', 'city',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('capital_cities', 'country',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
