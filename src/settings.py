from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Настройки сервера."""
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=[".env", "../.env"],
        env_file_encoding="utf-8",
    )


settings = Settings()
