import functools
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrestructure.repository.sql.UserCostumerRepository import UserCostumerRepository
from app.shared.encrypt import salty_password
from app.shared.models.database import UserCustomer
from app.shared.scheme.user import UserRequest


class UserService:
    def __init__(self):
        self.users_repository = UserCostumerRepository()

    async def get(self, session: AsyncSession, usercode: int) -> UserCustomer | None:
        return await self.users_repository.get_user_by_usercode(session, usercode)

    async def create(self, session: AsyncSession, req: UserRequest) -> bool:
        salt, hashed_password = salty_password(req.password.get_secret_value())
        birth_date = datetime.combine(req.birth_date, datetime.min.time())

        user = UserCustomer(
            usercode=req.usercode,
            hashed_password=hashed_password,
            salt=salt,
            firstname=req.firstname,
            paternal_surname=req.paternal_surname,
            maternal_surname=req.maternal_surname,
            birth_date=birth_date,
            email=str(req.email),
            curp=req.curp,
            phone_number=req.phone_number,
            address=req.address
        )

        status = await self.users_repository.save(session, user)

        return status is not None

    async def delete(self, session: AsyncSession, code: int):
        pass


@functools.lru_cache
def get_user_service() -> UserService:
    return UserService()
