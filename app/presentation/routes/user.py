from fastapi import APIRouter

from app.shared.dependencies import UserDependency
from app.shared.scheme.user import UserRequest

user_router = APIRouter(
    prefix="/user",
    tags=["Customer User route"]
)


@user_router.post("/")
async def create_user(user: UserRequest, user_dep: UserDependency):
    return await user_dep.create(user)
