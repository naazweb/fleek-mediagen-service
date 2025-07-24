from pydantic import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    # App Configuration
    PROJECT_NAME: str = "Fleek MediaGen Service"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    SECRET_KEY: str
    ALLOWED_HOSTS: list[str]
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

settings = Settings()
