"""reinitialize

Revision ID: bf4d174b94e1
Revises: 
Create Date: 2023-06-21 11:50:12.708259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf4d174b94e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('smershes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('smershes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_smershes_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_smershes_name'), ['name'], unique=True)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_name'), ['name'], unique=True)

    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('smersh_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['smersh_id'], ['smershes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('subjects', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_subjects_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_subjects_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_subjects_rating'), ['rating'], unique=False)

    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_a_id', sa.Integer(), nullable=False),
    sa.Column('subject_b_id', sa.Integer(), nullable=False),
    sa.Column('subject_a_win', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('voter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_a_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['subject_b_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['voter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_votes_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_votes_id'))

    op.drop_table('votes')
    with op.batch_alter_table('subjects', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_subjects_rating'))
        batch_op.drop_index(batch_op.f('ix_subjects_name'))
        batch_op.drop_index(batch_op.f('ix_subjects_id'))

    op.drop_table('subjects')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_name'))
        batch_op.drop_index(batch_op.f('ix_users_id'))

    op.drop_table('users')
    with op.batch_alter_table('smershes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_smershes_name'))
        batch_op.drop_index(batch_op.f('ix_smershes_id'))

    op.drop_table('smershes')
    # ### end Alembic commands ###