import functools

from app import ResponseException
from app.domain.service.user import get_user_service
from app.shared.scheme import StatusMessage, StatusSuccess, StatusFailure
from app.shared.scheme.user import UserRequest


class UserUseCase:
    def __init__(self):
        self.user_service = get_user_service()

    async def create(self, user: UserRequest) -> StatusMessage:
        status = await self.user_service.create(user)

        return StatusSuccess() if status else StatusFailure()

    async def delete(self, code: int, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise ResponseException("Invalid code.")

        return StatusSuccess()


@functools.lru_cache
def get_user_use_case() -> UserUseCase:
    return UserUseCase()
