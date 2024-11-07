"""Corrigindo campo created_at para datetime. Adicionado campo updated_at no modelo User

Revision ID: dce6f7b46c6e
Revises: 7b4cf720d2e1
Create Date: 2024-09-05 02:19:27.329791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dce6f7b46c6e'
down_revision: Union[str, None] = '7b4cf720d2e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    op.execute('''
        ALTER TABLE users 
        ALTER COLUMN created_at 
        TYPE TIMESTAMP WITHOUT TIME ZONE 
        USING created_at::timestamp without time zone
    ''')

    op.add_column(
        'users',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'), 
            onupdate=sa.text('(CURRENT_TIMESTAMP)'), 
            nullable=False
        )
    )


def downgrade() -> None:
    
    op.drop_column(
        'users', 
        'updated_at'
    )

    op.alter_column(
        'users',
        'created_at',
        type_=sa.String(),
    )
