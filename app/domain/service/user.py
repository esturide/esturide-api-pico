import functools
from datetime import datetime

from app.infrestructure.repository.user import UserRepository
from app.shared.encrypt import salty_password
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.user import UserRequest


class UserService(metaclass=Singleton):
    def __init__(self):
        self.user_repository = UserRepository()

    async def get(self, code: int):
        return await UserRepository.get_user_by_code(code)

    async def create(self, req: UserRequest):
        salt, hashed_password = salty_password(req.password.get_secret_value())
        birth_date = datetime.combine(req.birth_date, datetime.min.time())

        user = User(
            code=req.code,
            first_name=req.first_name,
            paternal_surname=req.paternal_surname,
            maternal_surname=req.maternal_surname,
            birth_date=birth_date,
            email=req.email,
            curp=req.curp,
            phone_number=req.phone_number,
            hashed_password=hashed_password,
            salt=salt,
        )

        return await self.user_repository.save(user)

    async def delete(self, code: int):
        pass
