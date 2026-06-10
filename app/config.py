from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core app settings
    PROJECT_NAME: str = "MedBrief"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # DB settings
    POSTGRES_DSN: PostgresDsn | None = None
    REDIS_DSN: RedisDsn | None = None

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    ) 

    @field_validator("POSTGRES_DSN", "REDIS_DSN", mode="before")
    @classmethod
    def assemble_dsn_strings(cls, v: any) -> str:
        if isinstance(v, str):
            return v
        return str(v)
    
settings = Settings()