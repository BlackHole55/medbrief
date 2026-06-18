from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from app.schemas import NoteCreatedOut, NoteCreatedIn, NoteOut
from app.models import NoteMdl, SummaryMdl, SummaryStatus
from app.db import get_db
from app.workers import generate_summary_task

router = APIRouter(prefix="/notes", tags=["Notes"])

# TODO: fix Broken object level authorization using authorization of integrated system
@router.post("", response_model=NoteCreatedOut, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreatedIn, db: AsyncSession = Depends(get_db)):
    new_note = NoteMdl(
        doctor_id=payload.doctor_id,
        patient_id=payload.patient_id,
        clinical_text=payload.clinical_text,
    )
    db.add(new_note)
    await db.flush()

    pending_summary = SummaryMdl(
        note_id=new_note.id,
        status=SummaryStatus.PENDING,
        patient_text=None,
    )
    db.add(pending_summary)

    await db.commit()
    await db.refresh(new_note, attribute_names=["summary"])

    generate_summary_task.delay(str(new_note.id))
    print(f"[STUB] Enqueued Celery task for note_id: {new_note.id}")

    return new_note

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(NoteMdl)
        .where(NoteMdl.id == note_id)
        .options(selectinload(NoteMdl.summary))
    )
    result = await db.execute(query)
    note = result.scalars().first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note

@router.get("/doctor/{doctor_id}", response_model=List[NoteOut])
async def list_doctor_notes(doctor_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(NoteMdl)
        .where(NoteMdl.doctor_id == doctor_id)
        .options(selectinload(NoteMdl.summary))
        .order_by(NoteMdl.created_at.desc())
    )
    result = await db.execute(query)
    notes = result.scalars().all()

    return notes