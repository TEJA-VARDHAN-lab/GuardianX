from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "GuardianX"
    API_VERSION: str = "v1"

    DATABASE_URL: str

    DEBUG: bool = True

    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()