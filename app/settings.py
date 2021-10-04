from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    database_url: str = "sqlite:///db.sqlite3"
    test_database_url: str = "sqlite:///test_db.sqlite3"
    secret_key: str = "my-secret-key"

    @validator("database_url")
    def parse_database_url(cls, value: str):
        return value.replace("postgres://", "postgresql://")


settings = Settings()
