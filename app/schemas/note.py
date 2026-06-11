from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from app.models import SummaryStatus
from app.schemas.summary import SummaryOut

class NoteCreated(BaseModel):
    doctor_id: UUID
    patient_id: UUID
    clinical_text: str = Field(
        ...,
        min_length=10,
        description="The raw, unedited medical record directly from the physician"
    )

    model_config = ConfigDict(from_attributes=True)

class NoteCreatedOut(BaseModel):
    id: UUID
    doctor_id: UUID
    patient_id: UUID
    summary_status: SummaryStatus = Field(default=SummaryStatus.PENDING)

    model_config = ConfigDict(from_attributes=True)

class NoteOut(BaseModel):
    id: UUID
    doctor_id: UUID
    patient_id: UUID
    clinical_text: str
    created_at: datetime
    summary: SummaryOut | None = None

    model_config = ConfigDict(from_attributes=True)