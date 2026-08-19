"""
Central place for all configuration values.
Everything is read from environment variables (or a local .env file)
so no secrets ever get hard-coded or committed to the repo.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Database ---
    # Example: postgresql://user:password@localhost:5432/origin26
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/origin26"

    # --- CORS ---
    # Your GitHub Pages frontend origin. Add more, comma separated, if needed.
    FRONTEND_ORIGIN: str = "https://arjitsingh0907.github.io"

    # --- Email (SMTP) ---
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_FROM_NAME: str = "ORIGIN '26 Team"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    # --- Admin access ---
    # Simple shared-secret key to protect the "list registrations" endpoint.
    ADMIN_API_KEY: str = "change-me"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
