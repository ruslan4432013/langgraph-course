from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = '.env'


class Settings(BaseSettings):
    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    OPENAI_API_KEY: SecretStr
    OPENAI_BASE_URL: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
