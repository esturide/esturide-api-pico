from fastapi import APIRouter, BackgroundTasks

from app.shared.dependencies import ScheduleDependency, AuthUserCodeAndRoleCredentials, GoogleMapsService
from app.shared.scheme import StatusMessage
from app.shared.scheme.schedule import ScheduleTravelFromAddressRequest

schedule_router = APIRouter(prefix="/travel", tags=["Travel Schedule route"])


@schedule_router.post("/", response_model=StatusMessage)
async def schedule_new_travel(schedule: ScheduleTravelFromAddressRequest, schedule_case: ScheduleDependency,
                              auth: AuthUserCodeAndRoleCredentials, gmaps: GoogleMapsService,
                              background_tasks: BackgroundTasks):
    code, role = auth
    return await schedule_case.create(schedule, code, role, gmaps, background_tasks)
