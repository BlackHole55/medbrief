from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from app.schemas import SummaryOut, SummaryApprove
from app.models import SummaryMdl, SummaryStatus, NoteMdl
from app.db import get_db

router = APIRouter(prefix="/summaries", tags=["Summaries"])

# TODO: fix Broken object level authorization using authorization of integrated system
@router.get("/{summary_id}", response_model=SummaryOut)
async def get_summary(summary_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(SummaryMdl)
        .where(SummaryMdl.id == summary_id)
    )
    result = await db.execute(query)
    summary = result.scalars().first()

    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    return summary

@router.patch("/{summary_id}/approve", response_model=SummaryOut)
async def approve_summary(summary_id: UUID, payload: SummaryApprove, db: AsyncSession = Depends(get_db)):
    query = (
        select(SummaryMdl)
        .where(SummaryMdl.id == summary_id)
    )
    result = await db.execute(query)
    summary = result.scalars().first()

    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    if summary.status != SummaryStatus.READY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve summary with status '{summary.status.value}'. It must be ready first."
        )
    
    summary.status = SummaryStatus.APPROVED
    summary.approved_by = payload.approved_by
    summary.approved_at = datetime.now(timezone.utc)

    await db.commit
    await db.refresh(summary)

    return summary

@router.get("/doctor/patient/{patient_id}/history", response_model=List[SummaryOut])
async def list_patient_summaries_for_doctor(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(SummaryMdl)
        .join(SummaryMdl.note)
        .where(NoteMdl.patient_id == patient_id)
        .order_by(SummaryMdl.generated_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()