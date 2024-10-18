"""Adicionando campos created_at updated_at na tabela de tarefas

Revision ID: fd951f6005b8
Revises: 6af3865bfa1a
Create Date: 2024-10-17 22:20:01.178960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd951f6005b8'
down_revision: Union[str, None] = '6af3865bfa1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos') as batch_op:
        batch_op.add_column(
            sa.Column(
                'created_at',
                sa.DateTime(),
                server_default=sa.text('(CURRENT_TIMESTAMP)'), 
                nullable=False
            )
        )

        batch_op.add_column(
            sa.Column(
                'updated_at',
                sa.DateTime(),
                server_default=sa.text('(CURRENT_TIMESTAMP)'), 
                onupdate=sa.text('(CURRENT_TIMESTAMP)'), 
                nullable=False
            )
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'updated_at')
    op.drop_column('todos', 'created_at')
    # ### end Alembic commands ###