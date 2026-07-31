from app.infrestructure.repository.client.db import ClientDocumentRepository
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton


class UserRepository(ClientDocumentRepository, metaclass=Singleton):
    async def get(self, *args, **kwargs) -> UserDocument | None:
        raise NotImplementedError()

    async def get_user_by_code(self, code: int) -> UserDocument | None:
        return await UserDocument.find_one(UserDocument.code == code)
