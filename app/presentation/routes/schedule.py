import datetime

from fastapi import APIRouter

from app.core.exception import UnauthorizedAccessException
from app.shared.dependencies import ScheduleDependency, AuthUserCodeCredentials, UserIsAuthenticated, \
    AuthUserCodeAndRoleCredentials
from app.shared.scheme import StatusMessage, StatusResponse
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelRequest, ScheduleTravelResponse, ScheduleTravelUpdateRequest
from app.shared.types.enum import Status

schedule_router = APIRouter(prefix="/schedule", tags=["Schedule travels"])


@schedule_router.post("/", response_model=StatusMessage)
async def schedule_new_travel(schedule: ScheduleTravelRequest, schedule_case: ScheduleDependency,
                              auth_user: AuthUserCodeCredentials):
    return await schedule_case.create(schedule, auth_user)


@schedule_router.get("/", response_model=StatusResponse[list[ScheduleTravelResponse]])
async def get_all_schedule(limit: int, schedule_case: ScheduleDependency, is_auth: UserIsAuthenticated):
    if not is_auth:
        raise UnauthorizedAccessException()

    all_schedule = await schedule_case.get_all(limit)

    return {
        "status": Status.success,
        "data": all_schedule,
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


@schedule_router.get("/current", response_model=StatusResponse[ScheduleTravelResponse])
async def get_current_schedule(schedule_case: ScheduleDependency, auth_user: AuthUserCodeCredentials):
    schedule = await schedule_case.get_current(auth_user)

    return {
        "status": Status.success,
        "data": schedule,
    }


@schedule_router.put("/")
async def update_current_schedule(req: ScheduleTravelUpdateRequest, schedule_case: ScheduleDependency,
                                  user_auth: AuthUserCodeAndRoleCredentials):
    code, role = user_auth

    return await schedule_case.update(code, role, req)
