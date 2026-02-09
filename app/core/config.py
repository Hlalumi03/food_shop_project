from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./food_shop.db"
    ECHO_SQL: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    API_BASE_URL: str = "http://localhost:8000"
    PROJECT_NAME: str = "Food Shop API"
    PROJECT_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
