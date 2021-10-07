"""create instances table

Revision ID: 5271f328ca75
Revises: 
Create Date: 2021-10-06 19:52:50.579452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5271f328ca75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("instances",
        sa.Column("id", sa.String(length=50)),
        sa.Column("container_id", sa.String(length=64), nullable=False),
        sa.Column("port", sa.Integer, nullable=False),
        sa.Column("protocol", sa.Enum("udp", "tcp", name="protocols"), nullable=False),
        sa.Column("volume_name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("instances")
