import functools

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import NotFoundException, UnauthorizedAccessException
from app.domain.service.user import UserService
from app.shared.scheme import StatusMessage, StatusSuccess, StatusFailure
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest, UserResponse, UserProfile


class UserUseCase:
    def __init__(self):
        self.user_service = UserService()

    async def create(self, session: AsyncSession, user: UserRequest) -> StatusMessage:
        status = await self.user_service.create(session, user)

        return StatusSuccess() if status else StatusFailure()

    async def update(self, session: AsyncSession, code: int, req: ProfileUpdateRequest, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise UnauthorizedAccessException("Invalid code.")

        return StatusFailure()

    async def delete(self, session: AsyncSession, code: int, auth_user: int) -> StatusMessage:
        if not code == auth_user:
            raise UnauthorizedAccessException("Invalid code.")

        return StatusFailure()

    async def get(self, session: AsyncSession, usercode: int) -> UserResponse:
        user = await self.user_service.get(usercode)

        if not user:
            raise NotFoundException("User not found.")

        return UserResponse(
            code=usercode,
            firstName=user.firstname,
            maternalSurname=user.maternal_surname,
            paternalSurname=user.paternal_surname,
            email=EmailStr(user.email),
            role=user.role,
        )

    async def get_profile(self, session: AsyncSession, code: int) -> UserProfile:
        user = await self.user_service.get(code)

        if not user:
            raise NotFoundException("User not found.")

        return UserProfile(
            usercode=code,
            firstName=user.firstname,
            maternalSurname=user.maternal_surname,
            paternalSurname=user.paternal_surname,
            curp=user.curp,
            birthDate=user.birth_date,
            phoneNumber=PhoneNumber(user.phone_number),
            email=EmailStr(user.email),
            address=user.address
        )


@functools.lru_cache
def get_user_use_case() -> UserUseCase:
    return UserUseCase()
