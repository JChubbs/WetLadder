"""create client foreign key to obfuscators

Revision ID: 23fc917d5820
Revises: d503bdcd6d4b
Create Date: 2021-12-02 22:02:19.608315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23fc917d5820'
down_revision = 'd503bdcd6d4b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("clients", schema=None) as batch_op:
        batch_op.add_column(sa.Column("obfuscator_id", sa.String(length=36), nullable=True))
        batch_op.create_foreign_key("clients_obfuscator_id_fk", "obfuscators", ["obfuscator_id"], ["id"], ondelete="CASCADE")

def downgrade():
    with op.batch_alter_table("clients", schema=None) as batch_op:
        batch_op.drop_column("obfuscator_id")
