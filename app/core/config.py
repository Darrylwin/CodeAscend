from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://codeascend:password@codeascend-database-kis8l0:5432/codeascend?sslmode=disable"
    
    # JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    # Durée de vie de l'access token en minutes (15 jours)
    access_token_expire_minutes: int = 15 * 24 * 60  # 21600 minutes
    
    # App
    app_name: str = "Quiz Programming API"
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()