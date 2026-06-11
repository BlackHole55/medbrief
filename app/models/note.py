from typing import TYPE_CHECKING
from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, text
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.models.summary import SummaryMdl

class NoteMdl(Base):
    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    doctor_id: Mapped[UUID] = mapped_column(index=True, nullable=False)
    patient_id: Mapped[UUID] = mapped_column(index=True, nullable=False)
    clinical_text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)")
    )

    summary: Mapped["SummaryMdl"] = relationship(
        "SummaryMdl",
        back_populates="note",
        uselist=False,
        cascade="all, delete-orphan"
    )