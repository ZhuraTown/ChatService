from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class TimestampMixin(SQLModel):
    created_at: Optional[datetime] = Field(
        None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )
    )
    updated_at: Optional[datetime] = Field(
        None,
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), nullable=True
        )
    )
    deleted_at: datetime = Field(default_factory=datetime.utcnow, nullable=True)


class OIDMixin(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
