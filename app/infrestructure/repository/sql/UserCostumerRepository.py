from select import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.models.database import UserCustomer


class UserCostumerRepository:
    @staticmethod
    async def get_user_by_usercode(session: AsyncSession, usercode: int) -> UserCustomer | None:
        stmt = select(UserCustomer).where(UserCustomer.usercode == usercode)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def save(session: AsyncSession, user: UserCustomer):
        session.add(user)

        await session.commit()
