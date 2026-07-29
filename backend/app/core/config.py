from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "GuardianX"
    API_VERSION: str = "v1"
    DATABASE_URL: str = "sqlite:///guardianx.db"
    DEBUG: bool = True
    SECRET_KEY: str = "guardianx-change-this-secret"

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()