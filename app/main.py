from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import notes_router, summaries_router, patient_summaries_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend service for AI-generated medical note summaries.",
    version=settings.VERSION
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_method=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

app.include_router(notes_router, prefix=settings.API_V1_STR)
app.include_router(summaries_router, prefix=settings.API_V1_STR)
app.include_router(patient_summaries_router, prefix=settings.API_V1_STR)