from app.infrestructure.repository.session import AsyncSessionRepository
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton


class UserRepository(AsyncSessionRepository, metaclass=Singleton):
    async def get(self, *args, **kwargs) -> User | None:
        raise NotImplementedError()

    async def get_user_by_code(self, code: int) -> User | None:
        return await User.find_one(User.code == code)
