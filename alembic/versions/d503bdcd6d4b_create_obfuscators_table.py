"""create obfuscators table

Revision ID: d503bdcd6d4b
Revises: 8cf6b8824a83
Create Date: 2021-11-21 20:19:29.040681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd503bdcd6d4b'
down_revision = '8cf6b8824a83'
branch_labels = None
depends_on = None


def upgrade():
    obfuscation_methods_enum = sa.Enum(
        "Replicant", 
        "Optimizer", 
        "shadow",
        "meeklite",
        "obfs4",
        "Dust",
        "obfs2",
        name="obfuscation_methods"
    )

    op.create_table("obfuscators",
        sa.Column("id", sa.String(length=36)),
        sa.Column("obfuscation_method", obfuscation_methods_enum, nullable=False),
        sa.Column("instance_id", sa.String(length=50), nullable=False),
        sa.Column("config", sa.Text()),
        sa.Column("listener_port", sa.Integer()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(["instance_id"], ["instances.id"], ondelete="CASCADE")
    )


def downgrade():
    op.drop_table("obfuscators")