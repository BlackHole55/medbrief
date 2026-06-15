from app.routers.notes import router as notes_router
from app.routers.summaries import router as summaries_router
from app.routers.patient_summaries import router as patient_summaries_router

__all__ = [
    "notes_router",
    "summaries_router",
    "patient_summaries_router"
]