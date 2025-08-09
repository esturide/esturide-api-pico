import functools

from app.domain.service.user import get_user_service
from app.shared.scheme import StatusMessage, StatusSuccess, StatusFailure
from app.shared.scheme.user import UserRequest


class UserUseCase:
    def __init__(self):
        self.user_service = get_user_service()

    async def create(self, user: UserRequest) -> StatusMessage:
        status = await self.user_service.create(user)

        return StatusSuccess() if status else StatusFailure()

    async def delete(self, code: int) -> StatusMessage:
        pass



@functools.lru_cache
def get_user_use_case() -> UserUseCase:
    return UserUseCase()
