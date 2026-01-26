from fastapi import APIRouter, BackgroundTasks

from app.shared.dependencies import ScheduleDependency, AuthUserCodeCredentials, UserIsAuthenticated, \
    AuthUserCodeAndRoleCredentials, GoogleMapsService
from app.shared.scheme import StatusMessage, StatusResponse
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelResponse, ScheduleTravelUpdateRequest, \
    ScheduleTravelFromAddressRequest
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import Status

schedule_router = APIRouter(prefix="/travel", tags=["Travel Schedule route"])


@schedule_router.post("/", response_model=StatusMessage)
async def schedule_new_travel(schedule: ScheduleTravelFromAddressRequest, schedule_case: ScheduleDependency,
                              auth: AuthUserCodeAndRoleCredentials, gmaps: GoogleMapsService,
                              background_tasks: BackgroundTasks):
    code, role = auth
    return await schedule_case.create(schedule, code, role, gmaps, background_tasks)


@schedule_router.get("/current", response_model=StatusResponse[ScheduleTravelStatusResponse])
async def get_current_schedule(schedule_case: ScheduleDependency, code: AuthUserCodeCredentials):
    schedule = await schedule_case.get_current(code)

    return {
        "status": Status.success,
        "data": schedule,
    }


@schedule_router.post("/update")
async def update_current_schedule(req: ScheduleTravelUpdateRequest, schedule_case: ScheduleDependency,
                                  user_auth: AuthUserCodeAndRoleCredentials) -> StatusMessage:
    code, role = user_auth

    return await schedule_case.update(code, role, req)
