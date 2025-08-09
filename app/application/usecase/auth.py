import functools

from app.domain.service.auth import get_auth_service
from app.shared.types import Token


class AuthUseCase:
    def __init__(self):
        self.auth_service = get_auth_service()

    async def login(self, code: int, password: str):
        token = await self.auth_service.authenticate(
            code,
            password
        )

        return token

    async def check(self, token: Token):
        return await self.auth_service.validate(token)

    async def refresh(self, token: Token):
        return await self.auth_service.refresh(token)


@functools.lru_cache
def get_auth_case() -> AuthUseCase:
    return AuthUseCase()
