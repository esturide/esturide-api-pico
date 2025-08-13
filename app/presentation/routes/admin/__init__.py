from fastapi import APIRouter

from app.shared.dependencies import AuthUserCodeCredentials, AdminManagerDependency
from app.shared.scheme.admin.schedule import ChangesScheduleRequest

admin_route = APIRouter(
    prefix="/admin",
    tags=["Admin Manager router"]
)


@admin_route.put("/schedule")
async def get_schedule(req: ChangesScheduleRequest, code: AuthUserCodeCredentials, admin: AdminManagerDependency):
    return await admin.change_schedule(code, req)
