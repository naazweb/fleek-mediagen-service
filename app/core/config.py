from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # Database Configuration
    DATABASE_URL: str
    
    # Celery Configuration
    CELERY_BROKER_URL: str 
    CELERY_RESULT_BACKEND: str 
    
    # Cloudflare Configuration
    CLOUDFLARE_ACCOUNT_ID: str
    CLOUDFLARE_API_TOKEN: str
    CLOUDFLARE_R2_BUCKET: str
    CLOUDFLARE_R2_ACCESS_KEY: str
    CLOUDFLARE_R2_SECRET_KEY: str
    CLOUDFLARE_R2_ENDPOINT: str
    
    # Replicate Configuration
    REPLICATE_API_TOKEN: str 
    
    @property
    def tortoise_config(self):
        return {
            "connections": {
                "default": self.DATABASE_URL
            },
            "apps": {
                "models": {
                    "models": ["app.models.media_gen", "aerich.models"],
                    "default_connection": "default",
                }
            }
        }

    

settings = Settings(_env_file=".env")
