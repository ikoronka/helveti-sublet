from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./helveti.db"
    ollama_url: str = "http://localhost:11434/api/generate"

    class Config:
        env_file = ".env"


settings = Settings()
