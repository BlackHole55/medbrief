from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from app.models import SummaryStatus
from datetime import datetime

class SummaryOut(BaseModel):
    id: UUID
    note_id: UUID
    patient_text: str | None = Field(default=None, description="The plain-language medical translation")
    status: SummaryStatus
    approved_by: UUID | None = None
    approved_at: datetime | None = None
    generated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class PatientSummaryOut(BaseModel):
    id: UUID
    patient_text: str | None = Field(default=None, description="The plain-language medical translation")
    status: SummaryStatus
    generated_at: datetime | None = None
    show_original: bool = Field(
        default=True,
        description="Dynamic flag indicating if this clinic/doctor exposes raw notes to patients"
    )
    clinical_text: str | None = Field(
        default=None,
        description="The raw doctor note, only populated if show_original is True"
    )
    model_config = ConfigDict(from_attributes=True)

class SummaryApprove(BaseModel):
    approved_by: UUID = Field(..., description="The ID of the clinical doctor authorizing this change")