from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Motor de Preços 2.0"
    DEBUG: bool = False  # <--- Adicione esta linha
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"

    class Config:
        env_file = ".env"


settings = Settings()
