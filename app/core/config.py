from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Chat Message API"
    debug: bool = True
    database_url: str = Field(default="sqlite:///./data.db", env="DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()
