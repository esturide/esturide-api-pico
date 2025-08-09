from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    db_credential: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')



@lru_cache
def get_settings():
    return DefaultSettings()
