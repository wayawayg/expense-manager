from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )
