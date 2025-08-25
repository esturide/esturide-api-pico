import functools

from app.core.exception import UnauthorizedAccessException, InvalidRequestException
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
        user, role = await self.auth_service.get_user_credentials_from_token(token)

        return await self.auth_service.refresh(user, role)

    async def get_session_role(self, token: Token) -> RoleUser:
        user, current_role = await self.auth_service.get_user_credentials_from_token(token)

        return current_role

    async def set_session_role(self, token: Token, req: RoleUpdateRequest) -> Token:
        role = req.role
        user, current_role = await self.auth_service.get_user_credentials_from_token(token)

        if not user.is_verified:
            raise UnauthorizedAccessException("User is not verified to make that change.")

        if current_role == role:
            raise InvalidRequestException("The user has the same requested role.")

        if role in [RoleUser.staff, RoleUser.admin]:
            if not user.is_valid_admin and role == RoleUser.admin:
                raise UnauthorizedAccessException("The user does not have administrator permissions.")
            elif not user.is_valid_staff and role == RoleUser.staff:
                raise UnauthorizedAccessException("The user does not have staff permissions.")

        return await self.auth_service.refresh(user, role)


@functools.lru_cache
def get_auth_session_case() -> AuthSessionUseCase:
    return AuthSessionUseCase()
