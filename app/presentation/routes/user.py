from fastapi import APIRouter

from app.shared.dependencies import UserDependency, AuthUserCodeCredentials, AdminAuthenticated
from app.shared.scheme import StatusMessage
from app.shared.scheme.user import UserRequest, ProfileUpdateRequest, UserResponse
from app.shared.types.enum import Status

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
    status = await user_dep.set_status(code, user, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "User profile updated successfully."
        }

    return {
        "status": Status.failure,
        "message": "User profile update failed."
    }


@user_router.delete('/{code}', response_model=StatusMessage)
async def delete_user(code: int, user_dep: UserDependency, auth_user: AuthUserCodeCredentials,
                      is_admin: AdminAuthenticated):
    status = await user_dep.delete(code, auth_user.code, is_admin)

    if status:
        return {
            "status": Status.success,
            "message": "User is deleted."
        }

    return {
        "status": Status.failure,
        "message": "User is not deleted."
    }