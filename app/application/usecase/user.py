import functools

from app.core.exception import NotFoundException, UnauthorizedAccessException
from app.domain.service.user import get_user_service
from app.shared.scheme import StatusMessage, StatusSuccess, StatusFailure
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest, UserResponse, UserProfile


class UserUseCase:
    def __init__(self):
        self.user_service = get_user_service()

    async def create(self, user: UserRequest) -> StatusMessage:
        status = await self.user_service.create(user)

        return StatusSuccess() if status else StatusFailure()

    async def update(self, code: int, req: ProfileUpdateRequest, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise UnauthorizedAccessException("Invalid code.")

        return StatusFailure()

    async def delete(self, code: int, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise UnauthorizedAccessException("Invalid code.")

        return StatusFailure()

    async def get(self, code: int) -> UserResponse:
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

    async def get_profile(self, code: int) -> UserProfile:
        user = await self.user_service.get(code)

        if not user:
            raise NotFoundException("User not found.")

        return UserProfile(
            code=code,
            firstName=user.first_name,
            maternalSurname=user.maternal_surname,
            paternalSurname=user.paternal_surname,
            curp=user.curp,
            birthDate=user.birth_date,
            phoneNumber=user.phone_number,
            email=user.email,
            role=user.role,
        )


@functools.lru_cache
def get_user_use_case() -> UserUseCase:
    return UserUseCase()
