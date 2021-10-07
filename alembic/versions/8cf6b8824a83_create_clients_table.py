"""create clients table

Revision ID: 8cf6b8824a83
Revises: 5271f328ca75
Create Date: 2021-10-06 20:05:00.153902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cf6b8824a83'
down_revision = '5271f328ca75'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("clients",
        sa.Column("id", sa.String(length=50)),
        sa.Column("instance_id", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id', 'instance_id'),
        sa.ForeignKeyConstraint(["instance_id"], ["instances.id"], ondelete="CASCADE")
    )


def downgrade():
    op.drop_table("clients")
