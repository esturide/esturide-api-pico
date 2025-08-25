import functools

from app.core import get_settings
from app.core.exception import UnauthorizedAccessException
from app.core.oauth2 import encode, decode
from app.infrestructure.repository.user import UserRepository
from app.shared.models.user import User
from app.shared.types import Token
from app.shared.types.enum import RoleUser


class AuthenticationCredentialsService:
    def __init__(self):
        self.settings = get_settings()

    async def get_user_if_authorized(self, code: int, password: str) -> User:
        user = await UserRepository.get_user_by_code(code)

        if user is None:
            raise UnauthorizedAccessException(
                detail="Invalid authentication credentials.",
            )

        if not user.same_password(password):
            raise UnauthorizedAccessException(
                detail="Invalid Password.",
            )

        return user

    async def get_user_credentials_from_token(self, token: str) -> tuple[User, RoleUser]:
        decode_data = decode(token, self.settings.secret_key, self.settings.algorithm)
        code = decode_data.get("code")
        role = decode_data.get("role")

        user = await UserRepository.get_user_by_code(code)

        if user is None:
            raise UnauthorizedAccessException(
                detail="Invalid authentication credentials.",
            )

        return user, RoleUser(role)

    async def authenticate(self, code: int, password: str) -> Token:
        user = await self.get_user_if_authorized(code, password)

        data = {
            "code": user.code,
            "role": user.role,
        }

        return encode(
            data,
            self.settings.access_token_expire_minutes,
            self.settings.secret_key,
            self.settings.algorithm
        )

    async def validate(self, token: Token):
        user, role = await self.get_user_credentials_from_token(token)

        if user is None:
            return False

        return True

    async def refresh(self, user: User, role: RoleUser) -> Token:
        data = {
            "code": user.code,
            "role": role.value,
        }

        return encode(
            data,
            self.settings.access_token_expire_minutes,
            self.settings.secret_key,
            self.settings.algorithm
        )


@functools.lru_cache
def get_auth_service() -> AuthenticationCredentialsService:
    return AuthenticationCredentialsService()
