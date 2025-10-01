from app.infrestructure.repository.firebase import AsyncSessionRepository
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.utils import async_task


class UserRepository(AsyncSessionRepository, metaclass=Singleton):
    async def get(self, *args, **kwargs) -> User | None:
        raise NotImplementedError()

    async def get_user_by_code(self, code: int) -> User | None:
        def get_user(c) -> User:
            return User.collection.filter("code", "==", c).get()

        return await async_task(get_user, code)
