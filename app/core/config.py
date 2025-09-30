import typing
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    db_cache_host: str
    db_cache_port: int
    db_cache_password: str

    db_sql_instance: str
    db_sql_name: str
    db_sql_password: str
    db_sql_user: str

    db_firebase_credential: str

    google_application_credentials: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    api_google_key: str

    origin_cors: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    @property
    def allowed_origins(self) -> typing.List[str]:
        return [o.strip() for o in self.origin_cors.split(',') if o.strip()]


@lru_cache
def get_settings() -> DefaultSettings:
    return DefaultSettings()
