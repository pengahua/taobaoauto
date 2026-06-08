from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Taobao Autopilot Commerce API"
    app_version: str = "0.1.0"
    environment: str = "local"
    database_url: str = "sqlite:///./taobao_autopilot.db"
    audit_log_enabled: bool = True
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
