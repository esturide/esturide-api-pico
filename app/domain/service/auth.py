import functools

from app.core import get_settings
from app.core.exception import UnauthorizedAccessException
from app.core.oauth2 import encode, check_if_expired, secure_decode, decode
from app.infrestructure.repository.user import UserRepository
from app.shared.types import Token


class AuthenticationCredentialsService:
    def __init__(self):
        self.settings = get_settings()

    async def authenticate(self, code: int, password: str) -> Token:
        user = await UserRepository.get_user_by_code(code)
        if user is None:
            raise UnauthorizedAccessException(
                detail="Invalid authentication credentials.",
            )

        if not user.same_password(password):
            raise UnauthorizedAccessException(
                detail="Invalid Password.",
            )

        data = {
            "code": user.code,
        }

        return encode(
            data,
            self.settings.access_token_expire_minutes,
            self.settings.secret_key,
            self.settings.algorithm
        )

    async def validate(self, token: Token):
        decode_data = decode(token, self.settings.secret_key, self.settings.algorithm)
        user = await UserRepository.get_user_by_code(decode_data.get("code"))

        if user is None:
            return False

        return True

    async def refresh(self, token: Token) -> Token:
        decode_data = decode(token, self.settings.secret_key, self.settings.algorithm)
        user = await UserRepository.get_user_by_code(decode_data.get("code"))

        if user is None:
            raise UnauthorizedAccessException(
                detail="Invalid authentication credentials.",
            )

        data = {
            "code": user.code,
        }

        return encode(
            data,
            self.settings.access_token_expire_minutes,
            self.settings.secret_key,
            self.settings.algorithm
        )

    async def get_user_from_token(self, token: Token):
        if not check_if_expired(token, self.settings.secret_key, self.settings.algorithm):
            return False

        with secure_decode(token) as decoded:
            if code := decoded.get("code"):
                return await UserRepository.get_user_by_code(code)

        return False


@functools.lru_cache
def get_auth_service() -> AuthenticationCredentialsService:
    return AuthenticationCredentialsService()
