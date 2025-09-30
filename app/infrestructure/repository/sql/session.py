import contextlib

from sqlalchemy.ext.asyncio import AsyncSession


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    @contextlib.asynccontextmanager
    async def session_manager(self):
        yield self.session
        await self.session.commit()
