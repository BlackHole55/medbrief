from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from app.schemas import PatientSummaryOut, SummaryApprove
from app.models import SummaryMdl, SummaryStatus, NoteMdl
from app.db import get_db

router = APIRouter(prefix="/summaries", tags=["Summaries"])

# TODO: fix Broken object level authorization using authorization of integrated system
@router.get("/patient/{patient_id}", response_model=List[PatientSummaryOut])
async def list_patient_summaries(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(SummaryMdl)
        .join(SummaryMdl.note)
        .where(
            NoteMdl.patient_id == patient_id,
            SummaryMdl.status == SummaryStatus.APPROVED
        )
        .options(joinedload(SummaryMdl.note))
        .order_by(SummaryMdl.generated_at.desc())
    )

    result = await db.execute(query)
    summaries = result.scalars().all()

    ## TODO: add show_original logic
    return summaries

@router.get("/{summary_id}", response_model=PatientSummaryOut)
async def get_single_patient_summary(summary_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(SummaryMdl)
        .where(SummaryMdl.id == summary_id)
        .options(joinedload(SummaryMdl.note))
    )
    result = await db.execute(query)
    summary = result.scalars().first()

    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    if summary.status != SummaryStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This summary is still undergoing clinical review and is not yet available."
        )
    
    return summary