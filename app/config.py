from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tracker.db"
    secret_key: str = "a_very_secret_key_that_should_be_changed_in_production"
    access_token_expiration_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
