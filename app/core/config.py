import typing
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    api_google_key: str

    mongodb_uri: str

    allowed_origin_cors: str

    cache_host: str
    cache_password: str
    cache_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    @property
    def allowed_cors(self) -> typing.List[str]:
        return [o.strip() for o in self.allowed_origin_cors.split(',') if o.strip()]


@lru_cache
def get_settings():
    return DefaultSettings()
