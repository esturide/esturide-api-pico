import functools

from app.domain.service.auth import get_auth_service
from app.shared.scheme.user import RoleUpdateRequest
from app.shared.types import Token
from app.shared.types.enum import RoleUser


class AuthSessionUseCase:
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

    async def refresh(self, token: Token) -> Token:
        return await self.auth_service.refresh(token)

    async def get_session_role(self, token: Token) -> RoleUser:
        return await self.auth_service.get_current_role(token)

    async def set_session_role(self, token: Token, req: RoleUpdateRequest) -> Token:
        return await self.auth_service.change_current_role(token, req.role)


@functools.lru_cache
def get_auth_session_case() -> AuthSessionUseCase:
    return AuthSessionUseCase()
