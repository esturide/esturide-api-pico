from fastapi import APIRouter

from app.shared.dependencies import RideDependency, ScheduleDependency, AuthUserCodeCredentials
from app.shared.scheme import StatusMessage, StatusFailure, StatusSuccess

check_router = APIRouter(
    prefix="/check",
    tags=["Check router"]
)


@check_router.get('/find/ride', response_model=StatusMessage)
async def current_ride_found(ride: RideDependency, code: AuthUserCodeCredentials):
    is_found = await ride.find_ride_if_exist(code) is not None

    if is_found:
        return StatusSuccess(message="Ride found.")
    else:
        return StatusFailure(message="You don't have a current ride.")


@check_router.get('/find/schedule', response_model=StatusMessage)
async def current_schedule_found(schedule: ScheduleDependency, code: AuthUserCodeCredentials):
    is_found = await schedule.find_schedule_if_exist(code) is not None

    if is_found:
        return StatusSuccess(message='Schedule is found.')
    else:
        return StatusFailure(message="You don't have a current schedule.")
