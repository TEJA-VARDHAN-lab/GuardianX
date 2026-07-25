from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "GuardianX"
    API_VERSION: str = "v1"
    DEBUG: bool = True
    SECRET_KEY: str
    DATABASE_URL: str

    # Telegram Notification Settings
    TELEGRAM_BOT_TOKEN: str = "8717488605:AAHw0ns5qPj0hdhkGDDoFcqxQc8nuDDOXDw"
    TELEGRAM_CHAT_ID: str = "7965594981"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()