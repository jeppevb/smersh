"""initial auto

Revision ID: d2d80880fc27
Revises: 043b2a77155e
Create Date: 2023-06-20 13:18:59.657421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2d80880fc27'
down_revision = '043b2a77155e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subjects_id'), 'subjects', ['id'], unique=False)
    op.create_index(op.f('ix_subjects_name'), 'subjects', ['name'], unique=True)
    op.create_index(op.f('ix_subjects_rating'), 'subjects', ['rating'], unique=False)
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_a_id', sa.Integer(), nullable=True),
    sa.Column('subject_b_id', sa.Integer(), nullable=True),
    sa.Column('subject_a_win', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_a_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['subject_b_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['voter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_votes_id'), 'votes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_votes_id'), table_name='votes')
    op.drop_table('votes')
    op.drop_index(op.f('ix_subjects_rating'), table_name='subjects')
    op.drop_index(op.f('ix_subjects_name'), table_name='subjects')
    op.drop_index(op.f('ix_subjects_id'), table_name='subjects')
    op.drop_table('subjects')
    # ### end Alembic commands ###