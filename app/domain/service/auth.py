import functools

from app.core import get_settings
from app.core.exception import UnauthorizedAccessException, InvalidRequestException
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
        user_code = decode_data.get("code")
        role = decode_data.get("role")

        user = await UserRepository.get_user_by_code(user_code)

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

    async def refresh(self, token: Token) -> Token:
        user, role = await self.get_user_credentials_from_token(token)

        if user is None:
            raise UnauthorizedAccessException(
                detail="Invalid authentication credentials.",
            )

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

    async def get_current_role(self, token: Token) -> RoleUser:
        user, current_role = await self.get_user_credentials_from_token(token)

        return current_role

    async def change_current_role(self, token: Token, role: RoleUser):
        user, current_role = await self.get_user_credentials_from_token(token)

        if not user.is_verified:
            raise UnauthorizedAccessException("User is not verified to make that change.")

        if current_role == role:
            raise InvalidRequestException("The user has the same requested role.")

        if role in [RoleUser.staff, RoleUser.admin]:
            if not user.is_valid_admin and role == RoleUser.admin:
                raise UnauthorizedAccessException("The user does not have administrator permissions.")
            elif not user.is_valid_staff and role == RoleUser.staff:
                raise UnauthorizedAccessException("The user does not have staff permissions.")

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
