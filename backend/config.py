from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./helveti.db"

    class Config:
        env_file = ".env"


settings = Settings()
