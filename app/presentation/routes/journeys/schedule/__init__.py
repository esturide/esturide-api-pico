from fastapi import APIRouter

from app.shared.dependencies import ScheduleDependency, AuthUserCodeAndRoleCredentials, GoogleMapsService
from app.shared.scheme import StatusMessage, StatusResponse
from app.shared.scheme.schedule import ScheduleTravelFromAddressRequest, ScheduleTravelResponse
from app.shared.types.enum import Status

schedule_router = APIRouter(prefix="/travel", tags=["Travel Schedule route"])


@schedule_router.post("/", response_model=StatusMessage)
async def schedule_new_schedule_travel(schedule: ScheduleTravelFromAddressRequest, schedule_case: ScheduleDependency,
                                       auth: AuthUserCodeAndRoleCredentials, gmaps: GoogleMapsService):
    code, role = auth
    return await schedule_case.create(schedule, code, role, gmaps)


@schedule_router.get('/', response_model=StatusResponse[ScheduleTravelResponse])
async def get_current_schedule_travel(schedule_case: ScheduleDependency, auth: AuthUserCodeAndRoleCredentials):
    code, role = auth

    if schedule := await schedule_case.current(code, role):
        return {
            'status': Status.success,
            'data': schedule
        }
    else:
        return {
            'status': Status.failure,
            'data': None
        }


@schedule_router.post('/update')
async def cancel_current_schedule_travel(terminate: bool = False, cancel: bool = False):
    pass
