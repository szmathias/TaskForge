"""
Application configuration settings.

This module defines the configuration settings for the TaskForge application,
including database connection, JWT secret key, and token expiration.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or defaults.

    Attributes:
        database_url: SQLAlchemy database connection URL
        secret_key: Secret key for JWT token signing
        access_token_expiration_minutes: JWT token expiration time in minutes
    """
    database_url: str = "sqlite:///./tracker.db"
    secret_key: str = "a_very_secret_key_that_should_be_changed_in_production"
    access_token_expiration_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
