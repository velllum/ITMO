from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """- настройки """
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    # DB_URL: str

    WEB_HOST: str
    WEB_PORT: int
    WEB_ALLOW_ORIGINS: str
    WEB_DEBUG: bool
    WEB_RELOAD: bool
    WEB_SECRET_KEY: str

    @property
    def DATABASE_URL_ASYNCPG(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='./docker/env/dev/.env')


settings = Settings()
