from app.shared.models.user import User
from app.shared.utils import async_task


class UserRepository:
    @staticmethod
    async def get(*args, **kwargs) -> User | None:
        raise NotImplementedError()

    @staticmethod
    async def get_user_by_code(code: int) -> User:
        def get_user(c) -> User:
            return User.collection.filter("code", "==", c).get()

        return await async_task(get_user, code)

    @staticmethod
    async def save(user: User):
        def task_save(model):
            model.save()

        await async_task(task_save, user)

        return True
