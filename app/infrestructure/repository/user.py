from app.infrestructure.repository.client.db import ClientDocumentRepository
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton


class UserRepository(ClientDocumentRepository, metaclass=Singleton):
    async def get(self, *args, **kwargs) -> User | None:
        raise NotImplementedError()

    async def get_user_by_code(self, code: int) -> User | None:
        return await User.find_one(User.code == code)
