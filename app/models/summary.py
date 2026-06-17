from typing import TYPE_CHECKING
import enum
from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum, DateTime, text
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.models.note import NoteMdl

class SummaryStatus(str, enum.Enum):
    PENDING = "pending"
    READY = "ready"
    APPROVED = "approved"
    PUBLISHED = "published"
    GENERATING = "generating"
    FAILED = "failed"

class SummaryMdl(Base):
    __tablename__ = "summaries"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    note_id: Mapped[UUID] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    patient_text: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[SummaryStatus] = mapped_column(
        Enum(SummaryStatus), 
        default=SummaryStatus.PENDING,
        nullable=False
    )
    approved_by: Mapped[UUID | None] = mapped_column(nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)")
    )

    note: Mapped["NoteMdl"] = relationship("NoteMdl", back_populates="summary")