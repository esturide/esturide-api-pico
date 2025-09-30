from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.dependencies import UserDependency, AuthUserCodeCredentials, AsyncSessionDatabase, \
    get_session_sql_async_db
from app.shared.scheme import StatusMessage
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest, UserResponse

user_router = APIRouter(
    prefix="/user",
    tags=["User router"]
)


@user_router.post("/")
async def create_user(user: UserRequest, user_dep: UserDependency):
    async with get_session_sql_async_db() as session:
        return await user_dep.create(session, user)


@user_router.get('/{code}', response_model=UserResponse)
async def get_user(code: int, session: AsyncSessionDatabase, user_dep: UserDependency):
    return await user_dep.get(session, code)


@user_router.post('/{code}', response_model=StatusMessage)
async def update_user(code: int, user: ProfileUpdateRequest, session: AsyncSessionDatabase, user_dep: UserDependency,
                      auth_user: AuthUserCodeCredentials):
    return await user_dep.update(session, code, user, auth_user)


@user_router.post('/{code}', response_model=StatusMessage)
async def delete_user(code: int, session: AsyncSessionDatabase, user_dep: UserDependency, auth_user: AuthUserCodeCredentials):
    return await user_dep.delete(session, code, auth_user)
