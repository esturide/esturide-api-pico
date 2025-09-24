import functools

from app.core.exception import ResponseException, NotFoundException
from app.domain.service.user import get_user_service
from app.shared.scheme import StatusMessage, StatusSuccess, StatusFailure
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest, UserResponse


class UserUseCase:
    def __init__(self):
        self.user_service = get_user_service()

    async def create(self, user: UserRequest) -> StatusMessage:
        status = await self.user_service.create(user)

        return StatusSuccess() if status else StatusFailure()

    async def update(self, code: int, req: ProfileUpdateRequest, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise ResponseException("Invalid code.")

        return StatusFailure()

    async def delete(self, code: int, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise ResponseException("Invalid code.")

        return StatusFailure()

    async def get(self, code: int):
        user = await self.user_service.get(code)

        if not user:
            raise NotFoundException("User not found.")

        return UserResponse(
            code=code,
            firstName=user.first_name,
            maternalSurname=user.maternal_surname,
            paternalSurname=user.paternal_surname,
            email=user.email,
            role=user.role,
        )

@functools.lru_cache
def get_user_use_case() -> UserUseCase:
    return UserUseCase()
