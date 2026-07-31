import typing
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    env: str | None

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

    @property
    def is_production(self) -> bool:
        if self.env is None:
            return True

        w_env = self.env.upper()

        return not w_env in ('DEV', 'DEVELOPMENT')


@lru_cache
def get_settings():
    return DefaultSettings()
