from fastapi import APIRouter

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, RideDependency
from app.shared.scheme import StatusResponse, StatusMessage
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types import UUID
from app.shared.types.enum import Status

rides_router = APIRouter(prefix="/rides", tags=["Rides"])


@rides_router.post('/')
async def request_ride(schedule: UUID, seat: str, user_auth: AuthUserCodeAndRoleCredentials, ride: RideDependency) -> StatusMessage:
    code, role = user_auth

    return await ride.create(code, role, schedule, seat)


@rides_router.get('/', response_model=StatusResponse[RideTravelStatusResponse])
async def get_current_ride(user_auth: AuthUserCodeAndRoleCredentials, ride: RideDependency):
    code, role = user_auth
    data = await ride.current(code, role)

    return StatusResponse(
        status=Status.success,
        data=data
    )


@rides_router.delete('/over')
async def over_ride(schedule: UUID, user_auth: AuthUserCodeAndRoleCredentials, ride: RideDependency) -> StatusMessage:
    code, role = user_auth

    return await ride.over(code, role, schedule)


@rides_router.delete('/cancel')
async def cancel_ride(schedule: UUID, user_auth: AuthUserCodeAndRoleCredentials, ride: RideDependency) -> StatusMessage:
    code, role = user_auth

    return await ride.cancel(code, role, schedule)
