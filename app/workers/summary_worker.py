import asyncio
from uuid import UUID
from celery.utils.log import get_task_logger
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from app.models import NoteMdl, SummaryMdl, SummaryStatus
from app.db import get_worker_db
from app.celery_app import celery_app

logger = get_task_logger(__name__)

async def _run(note_id: UUID) -> None:
    """
    The async inner function that executes the core business logic.
    Operates within an isolated, worker-specific database session.
    """

    async with get_worker_db() as db:
        query = (
            select(NoteMdl)
            .where(NoteMdl.id == note_id)
            .options(selectinload(NoteMdl.summary))
        )
        result = await db.execute(query)
        note = result.scalars().first()

        if not note:
            logger.warning(f"Task aborted. Note {note_id} not found or was deleted.")
            return
        
        summary = note.summary
        if not summary:
            summary = SummaryMdl(note_id=note_id)
            db.add(summary)

        if summary.status == SummaryStatus.APPROVED:
            logger.info(f"Summary for note {note_id} is already APPROVED. Skipping.")
            return
        
        summary.status = SummaryStatus.GENERATING
        await db.commit()
        logger.info(f"Summary generation status set to GENERATING for note {note_id}")

        try:
            # patient_text = await anthropic_service.generate_patient_summary(
            #     clinical_text=note.clinical_text
            # )

            # summary.patient_text = patient_text
            # summary.status = SummaryStatus.READY
            # summary.generated_at = datetime.now(timezone.utc)

            # await db.commit()
            logger.info(f"Summary generation successfully COMPLETED for note {note_id}")
        except Exception as exc:
            logger.error(f"AI generation failed for note {note_id}: {str(exc)}")

            summary.status = SummaryStatus.FAILED
            await db.commit()

            raise exc
        
@celery_app.task(bind=True)
def generate_summary_task(self, note_id: str) -> None:
    """
    The synchronous Celery entry-point wrapper. 
    Manages the running async loop for this background worker thread.
    """
    logger.info(f"Starting Celery background worker task for note_id: {note_id}")
    
    parsed_uuid = UUID(note_id)

    asyncio.run(_run(parsed_uuid))