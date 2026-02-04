from datetime import datetime

from app.infrestructure.repository.user import UserRepository
from app.shared.encrypt import salty_password
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest


class UserService(metaclass=Singleton):
    def __init__(self):
        self.user_repository = UserRepository()

    async def get(self, code: int):
        return await self.user_repository.get_user_by_code(code)

    async def create(self, req: UserRequest):
        salt, hashed_password = salty_password(req.password.get_secret_value())
        birth_date = datetime.combine(req.birth_date, datetime.min.time())

        user = UserDocument(
            code=req.code,
            first_name=req.first_name,
            paternal_surname=req.paternal_surname,
            maternal_surname=req.maternal_surname,
            birth_date=birth_date,
            email=req.email,
            curp=req.curp,
            address=req.address,
            phone_number=req.phone_number,
            hashed_password=hashed_password,
            salt=salt,
            gender=req.gender
        )

        return await self.user_repository.save(user)

    async def update(self, req: ProfileUpdateRequest, user: UserDocument):
        if req.password:
            user.salt, user.hashed_password = salty_password(req.password.get_secret_value())

        if req.birth_date:
            user.birth_date = datetime.combine(req.birth_date, datetime.min.time())

        if req.first_name:
            user.first_name = req.first_name

        if req.maternal_surname:
            user.maternal_surname = req.maternal_surname

        if req.paternal_surname:
            user.paternal_surname = req.paternal_surname

        if req.curp:
            user.curp = req.curp

        return await self.user_repository.update(user)

    async def delete(self, user: UserDocument):
        user.deleted = True
        return await self.user_repository.update(user)

    async def banned(self, user: UserDocument):
        if not user.deleted:
            user.banned = True
        else:
            return False

        return await self.user_repository.update(user)
