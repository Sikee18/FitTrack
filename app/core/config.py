from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_SECRET: str | None = None
    REFRESH_EXPIRE_DAYS: int = 7

    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs/dev"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    APP_NAME: str = "Instaverify"
    ENV: str = "dev"
    DEBUG: bool = True

    class Config:
        env_file = ".env.development"
        extra = "ignore"

settings = Settings()
