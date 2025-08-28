"""
Application configuration management using Pydantic settings.
Handles environment variables and configuration validation.
"""

from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator
import os
from pathlib import Path

# Load .env file explicitly
from dotenv import load_dotenv
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"

load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./booking.db"
    
    # Email Configuration
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: EmailStr
    SMTP_FROM_NAME: str = "Event Booking Platform"
    SMTP_USE_TLS: bool = True
    
    # Security
    ALLOWED_ORIGINS: List[str] = ["http://localhost:4321", "http://localhost:3000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Business Configuration
    ADMIN_EMAIL: Optional[EmailStr] = None
    BUSINESS_NAME: str = "Event Booking Platform"
    BUSINESS_EMAIL: EmailStr
    BUSINESS_PHONE: Optional[str] = None
    
    # File Upload (for future gallery features)
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    UPLOAD_DIR: str = "uploads"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Ensure secret key is provided and secure."""
        if not v:
            raise ValueError("SECRET_KEY must be provided")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_origins(cls, v):
        """Parse ALLOWED_ORIGINS from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_hosts(cls, v):
        """Parse ALLOWED_HOSTS from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("ADMIN_EMAIL", pre=True)
    def set_admin_email(cls, v, values):
        """Set admin email to business email if not provided."""
        if not v and "BUSINESS_EMAIL" in values:
            return values["BUSINESS_EMAIL"]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentSettings(Settings):
    """Development environment settings."""
    DEBUG: bool = True
    
    class Config:
        env_file = ".env.development"


class ProductionSettings(Settings):
    """Production environment settings."""
    DEBUG: bool = False
    
    # Override with secure defaults for production
    ALLOWED_ORIGINS: List[str] = []  # Must be explicitly set
    
    class Config:
        env_file = ".env.production"


class TestSettings(Settings):
    """Test environment settings."""
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Disable email in tests
    SMTP_HOST: str = "localhost"
    SMTP_USERNAME: str = "test"
    SMTP_PASSWORD: str = "test"
    SMTP_FROM_EMAIL: EmailStr = "test@example.com"
    BUSINESS_EMAIL: EmailStr = "test@example.com"
    
    class Config:
        env_file = ".env.test"


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings based on environment.
    
    Returns:
        Settings: Configuration instance
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()


# Export settings instance for convenience
settings = get_settings()