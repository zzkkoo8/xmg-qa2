"""Create Support Foundation business state."""

from alembic import op

from xmg_qa2.infrastructure.db import models  # noqa: F401
from xmg_qa2.infrastructure.db.base import Base

revision = "0001_support_foundation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
