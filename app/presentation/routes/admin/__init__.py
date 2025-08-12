from fastapi import APIRouter


admin_route = APIRouter(
    prefix="/admin",
    tags=["Auth router"]
)
