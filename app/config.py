from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core app settings
    PROJECT_NAME: str = "MedBrief"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # DB settings
    POSTGRES_DSN: str | None = None
    CELERY_BROKER_URL: str | None = None
    CELERY_BACKEND_URL: str | None = None

    GEMINI_API_KEY: str | None = None

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    ) 

    @field_validator("POSTGRES_DSN", "CELERY_BROKER_URL", "CELERY_BACKEND_URL", mode="before")
    @classmethod
    def assemble_dsn_strings(cls, v: any) -> str:
        if isinstance(v, str):
            return v
        return str(v)
    
settings = Settings()