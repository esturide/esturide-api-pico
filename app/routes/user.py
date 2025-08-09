from fastapi import APIRouter

from app.models import User

user_router = APIRouter()


@user_router.get("/users/", tags=["users"])
async def create_user():
    u = User()
    u.name = "Azeem"
    u.age = 26
    u.save()

    return True
