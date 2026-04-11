from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LANGSMITH_TRACING: str = ""
    LANGSMITH_ENDPOINT: str = ""
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = ""
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    TAVILY_API_KEY: str = ""
    MCP_SERVER_URL: str = "http://localhost:8000"
    CALLBACK_URL: str = "http://localhost:9090/callback"

    model_config = SettingsConfigDict(
        env_file=[".env", "../.env"],
        env_file_encoding="utf-8",
    )


settings = Settings()
