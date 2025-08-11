from fastapi import APIRouter

from app.shared.dependencies import UserDependency, AuthUserCodeCredentials
from app.shared.scheme import StatusMessage
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest, UserResponse

user_router = APIRouter(
    prefix="/user",
    tags=["User router"]
)


@user_router.post("/")
async def create_user(user: UserRequest, user_dep: UserDependency):
    return await user_dep.create(user)


@user_router.get('/{code}', response_model=UserResponse)
async def get_user(code: int, user_dep: UserDependency):
    return await user_dep.get(code)


@user_router.put('/{code}', response_model=StatusMessage)
async def update_user(code: int, user: ProfileUpdateRequest, user_dep: UserDependency,
                      auth_user: AuthUserCodeCredentials):
    return await user_dep.update(code, user, auth_user)


@user_router.delete('/{code}', response_model=StatusMessage)
async def delete_user(code: int, user_dep: UserDependency, auth_user: AuthUserCodeCredentials):
    return await user_dep.delete(code, auth_user)
