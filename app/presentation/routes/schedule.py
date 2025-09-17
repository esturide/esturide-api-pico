import datetime

from fastapi import APIRouter, BackgroundTasks

from app.shared.dependencies import ScheduleDependency, AuthUserCodeCredentials, UserIsAuthenticated, \
    AuthUserCodeAndRoleCredentials, GoogleGeolocationDepend
from app.shared.scheme import StatusMessage, StatusResponse
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelResponse, ScheduleTravelUpdateRequest, \
    ScheduleTravelFromAddressRequest
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import Status

schedule_router = APIRouter(prefix="/schedule", tags=["Schedule travels"])


@schedule_router.post("/", response_model=StatusMessage)
async def schedule_new_travel(schedule: ScheduleTravelFromAddressRequest, schedule_case: ScheduleDependency,
                              auth: AuthUserCodeAndRoleCredentials, geocoder: GoogleGeolocationDepend,
                              background_tasks: BackgroundTasks):
    code, role = auth
    return await schedule_case.create(schedule, code, role, geocoder, background_tasks)


@schedule_router.get("/", response_model=StatusResponse[list[ScheduleTravelResponse]])
async def get_all_schedule(limit: int, schedule_case: ScheduleDependency, is_auth: UserIsAuthenticated):
    if is_auth:
        all_schedule = await schedule_case.get_all(limit)

        return {
            "status": Status.success,
            "data": all_schedule,
        }

    return {
        "status": Status.failure,
        "data": [],
    }


@schedule_router.post("/filtering", response_model=StatusResponse[list[ScheduleTravelResponse]])
async def filtering_schedule(options: FilteringOptionsRequest, limit: int, schedule_case: ScheduleDependency,
                             user_auth: AuthUserCodeAndRoleCredentials):
    code, role = user_auth

    results = await schedule_case.search(code, role, options, limit)

    return {
        "status": Status.success,
        "data": results,
    }


@schedule_router.get("/search", response_model=StatusResponse[list[ScheduleTravelResponse]])
async def search_schedule(
        schedule_case: ScheduleDependency,
        user_auth: AuthUserCodeAndRoleCredentials,
        terminate: bool = False,
        cancel: bool = False,
        starting: datetime.datetime | None = None,
        terminated: datetime.datetime | None = None,
        min_price: float = 1,
        max_price: float | None = None,
        limit: int = 10,
):
    code, role = user_auth
    options = FilteringOptionsRequest(
        terminate=terminate,
        cancel=cancel,
        starting=starting,
        terminated=terminated,
        min_price=min_price,
        max_price=max_price
    )

    results = await schedule_case.search(
        code,
        role,
        options,
        limit
    )

    return {
        "status": Status.success,
        "data": results,
    }


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
